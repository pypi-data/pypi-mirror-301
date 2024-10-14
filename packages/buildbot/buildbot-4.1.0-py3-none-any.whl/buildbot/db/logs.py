# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members


from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING

import sqlalchemy as sa
from twisted.internet import defer
from twisted.python import log

from buildbot.db import base
from buildbot.db.compression import BrotliCompressor
from buildbot.db.compression import BZipCompressor
from buildbot.db.compression import CompressorInterface
from buildbot.db.compression import GZipCompressor
from buildbot.db.compression import LZ4Compressor
from buildbot.db.compression import ZStdCompressor
from buildbot.warnings import warn_deprecated

if TYPE_CHECKING:
    from typing import Literal

    LogType = Literal['s', 't', 'h', 'd']


class LogSlugExistsError(KeyError):
    pass


class LogCompressionFormatUnavailableError(LookupError):
    pass


@dataclasses.dataclass
class LogModel:
    id: int
    name: str
    slug: str
    stepid: int
    complete: bool
    num_lines: int
    type: LogType

    # For backward compatibility
    def __getitem__(self, key: str):
        warn_deprecated(
            '4.1.0',
            (
                'LogsConnectorComponent '
                'getLog, getLogBySlug, and getLogs '
                'no longer return Log as dictionnaries. '
                'Usage of [] accessor is deprecated: please access the member directly'
            ),
        )

        if hasattr(self, key):
            return getattr(self, key)

        raise KeyError(key)


class RawCompressor(CompressorInterface):
    name = "raw"

    @staticmethod
    def dumps(data: bytes) -> bytes:
        return data

    @staticmethod
    def read(data: bytes) -> bytes:
        return data


class LogsConnectorComponent(base.DBConnectorComponent):
    # Postgres and MySQL will both allow bigger sizes than this.  The limit
    # for MySQL appears to be max_packet_size (default 1M).
    # note that MAX_CHUNK_SIZE is equal to BUFFER_SIZE in buildbot_worker.runprocess
    MAX_CHUNK_SIZE = 65536  # a chunk may not be bigger than this
    MAX_CHUNK_LINES = 1000  # a chunk may not have more lines than this

    NO_COMPRESSION_ID = 0
    COMPRESSION_BYID: dict[int, type[CompressorInterface]] = {
        NO_COMPRESSION_ID: RawCompressor,
        1: GZipCompressor,
        2: BZipCompressor,
        3: LZ4Compressor,
        4: ZStdCompressor,
        5: BrotliCompressor,
    }

    COMPRESSION_MODE = {
        compressor.name: (compressor_id, compressor)
        for compressor_id, compressor in COMPRESSION_BYID.items()
    }

    def _get_compressor(self, compressor_id: int) -> type[CompressorInterface]:
        compressor = self.COMPRESSION_BYID.get(compressor_id)
        if compressor is None:
            msg = f"Unknown compression method ID {compressor_id}"
            raise LogCompressionFormatUnavailableError(msg)
        if not compressor.available:
            msg = (
                f"Log compression method {compressor.name} is not available. "
                "You might be missing a dependency."
            )
            raise LogCompressionFormatUnavailableError(msg)
        return compressor

    def _getLog(self, whereclause) -> defer.Deferred[LogModel | None]:
        def thd_getLog(conn) -> LogModel | None:
            q = self.db.model.logs.select()
            if whereclause is not None:
                q = q.where(whereclause)
            res = conn.execute(q).mappings()
            row = res.fetchone()

            rv = None
            if row:
                rv = self._model_from_row(row)
            res.close()
            return rv

        return self.db.pool.do(thd_getLog)

    def getLog(self, logid: int) -> defer.Deferred[LogModel | None]:
        return self._getLog(self.db.model.logs.c.id == logid)

    def getLogBySlug(self, stepid: int, slug: str) -> defer.Deferred[LogModel | None]:
        tbl = self.db.model.logs
        return self._getLog((tbl.c.slug == slug) & (tbl.c.stepid == stepid))

    def getLogs(self, stepid: int | None = None) -> defer.Deferred[list[LogModel]]:
        def thdGetLogs(conn) -> list[LogModel]:
            tbl = self.db.model.logs
            q = tbl.select()
            if stepid is not None:
                q = q.where(tbl.c.stepid == stepid)
            q = q.order_by(tbl.c.id)
            res = conn.execute(q).mappings()
            return [self._model_from_row(row) for row in res.fetchall()]

        return self.db.pool.do(thdGetLogs)

    def getLogLines(self, logid: int, first_line: int, last_line: int) -> defer.Deferred[str]:
        def thdGetLogLines(conn) -> str:
            # get a set of chunks that completely cover the requested range
            tbl = self.db.model.logchunks
            q = sa.select(tbl.c.first_line, tbl.c.last_line, tbl.c.content, tbl.c.compressed)
            q = q.where(tbl.c.logid == logid)
            q = q.where(tbl.c.first_line <= last_line)
            q = q.where(tbl.c.last_line >= first_line)
            q = q.order_by(tbl.c.first_line)
            rv = []
            for row in conn.execute(q):
                # Retrieve associated "reader" and extract the data
                # Note that row.content is stored as bytes, and our caller expects unicode
                data = self._get_compressor(row.compressed).read(row.content)
                content = data.decode('utf-8')

                if row.first_line < first_line:
                    idx = -1
                    count = first_line - row.first_line
                    for _ in range(count):
                        idx = content.index('\n', idx + 1)
                    content = content[idx + 1 :]
                if row.last_line > last_line:
                    idx = len(content) + 1
                    count = row.last_line - last_line
                    for _ in range(count):
                        idx = content.rindex('\n', 0, idx)
                    content = content[:idx]
                rv.append(content)
            return '\n'.join(rv) + '\n' if rv else ''

        return self.db.pool.do(thdGetLogLines)

    def addLog(self, stepid: int, name: str, slug: str, type: LogType) -> defer.Deferred[int]:
        assert type in 'tsh', "Log type must be one of t, s, or h"

        def thdAddLog(conn) -> int:
            try:
                r = conn.execute(
                    self.db.model.logs.insert(),
                    {
                        "name": name,
                        "slug": slug,
                        "stepid": stepid,
                        "complete": 0,
                        "num_lines": 0,
                        "type": type,
                    },
                )
                conn.commit()
                return r.inserted_primary_key[0]
            except (sa.exc.IntegrityError, sa.exc.ProgrammingError) as e:
                conn.rollback()
                raise LogSlugExistsError(
                    f"log with slug '{slug!r}' already exists in this step"
                ) from e

        return self.db.pool.do(thdAddLog)

    def thdCompressChunk(self, chunk: bytes) -> tuple[bytes, int]:
        compress_method: str = self.master.config.logCompressionMethod
        # unknown compression method
        if compress_method not in self.COMPRESSION_MODE:
            return chunk, self.NO_COMPRESSION_ID

        compressed_id, compressor = self.COMPRESSION_MODE[compress_method]
        # compression method is not available (missing dependency most likely)
        if not compressor.available or compressed_id == self.NO_COMPRESSION_ID:
            return chunk, self.NO_COMPRESSION_ID

        compressed_chunk = compressor.dumps(chunk)
        # Is it useful to compress the chunk?
        if len(chunk) <= len(compressed_chunk):
            return chunk, self.NO_COMPRESSION_ID

        return compressed_chunk, compressed_id

    def thdSplitAndAppendChunk(
        self, conn, logid: int, content: bytes, first_line: int
    ) -> tuple[int, int]:
        # Break the content up into chunks.  This takes advantage of the
        # fact that no character but u'\n' maps to b'\n' in UTF-8.
        remaining: bytes | None = content
        chunk_first_line = last_line = first_line
        while remaining:
            chunk, remaining = self._splitBigChunk(remaining, logid)
            last_line = chunk_first_line + chunk.count(b'\n')

            chunk, compressed_id = self.thdCompressChunk(chunk)
            res = conn.execute(
                self.db.model.logchunks.insert(),
                {
                    "logid": logid,
                    "first_line": chunk_first_line,
                    "last_line": last_line,
                    "content": chunk,
                    "compressed": compressed_id,
                },
            )
            conn.commit()
            res.close()
            chunk_first_line = last_line + 1
        res = conn.execute(
            self.db.model.logs.update()
            .where(self.db.model.logs.c.id == logid)
            .values(num_lines=last_line + 1)
        )
        conn.commit()
        res.close()
        return first_line, last_line

    def thdAppendLog(self, conn, logid: int, content: str) -> tuple[int, int] | None:
        # check for trailing newline and strip it for storage -- chunks omit
        # the trailing newline
        assert content[-1] == '\n'
        # Note that row.content is stored as bytes, and our caller is sending unicode
        content_bytes = content[:-1].encode('utf-8')
        q = sa.select(self.db.model.logs.c.num_lines)
        q = q.where(self.db.model.logs.c.id == logid)
        res = conn.execute(q)
        num_lines = res.fetchone()
        res.close()
        if not num_lines:
            return None  # ignore a missing log

        return self.thdSplitAndAppendChunk(
            conn=conn, logid=logid, content=content_bytes, first_line=num_lines[0]
        )

    def appendLog(self, logid, content) -> defer.Deferred[tuple[int, int] | None]:
        def thdappendLog(conn) -> tuple[int, int] | None:
            return self.thdAppendLog(conn, logid, content)

        return self.db.pool.do(thdappendLog)

    def _splitBigChunk(self, content: bytes, logid: int) -> tuple[bytes, bytes | None]:
        """
        Split CONTENT on a line boundary into a prefix smaller than 64k and
        a suffix containing the remainder, omitting the splitting newline.
        """
        # if it's small enough, just return it
        if len(content) < self.MAX_CHUNK_SIZE:
            return content, None

        # find the last newline before the limit
        i = content.rfind(b'\n', 0, self.MAX_CHUNK_SIZE)
        if i != -1:
            return content[:i], content[i + 1 :]

        log.msg(f'truncating long line for log {logid}')

        # first, truncate this down to something that decodes correctly
        truncline = content[: self.MAX_CHUNK_SIZE]
        while truncline:
            try:
                truncline.decode('utf-8')
                break
            except UnicodeDecodeError:
                truncline = truncline[:-1]

        # then find the beginning of the next line
        i = content.find(b'\n', self.MAX_CHUNK_SIZE)
        if i == -1:
            return truncline, None
        return truncline, content[i + 1 :]

    def finishLog(self, logid: int) -> defer.Deferred[None]:
        def thdfinishLog(conn) -> None:
            tbl = self.db.model.logs
            q = tbl.update().where(tbl.c.id == logid)
            conn.execute(q.values(complete=1))

        return self.db.pool.do_with_transaction(thdfinishLog)

    def compressLog(self, logid: int, force: bool = False) -> defer.Deferred[int]:
        def thdcompressLog(conn) -> int:
            tbl = self.db.model.logchunks
            q = sa.select(
                tbl.c.first_line,
                tbl.c.last_line,
                sa.func.length(tbl.c.content),
                tbl.c.compressed,
            )
            q = q.where(tbl.c.logid == logid)
            q = q.order_by(tbl.c.first_line)

            rows = conn.execute(q)
            todo_gather_list = []
            numchunks = 0
            totlength = 0
            todo_numchunks = 0
            todo_first_line = 0
            todo_last_line = 0
            todo_length = 0
            # first pass, we fetch the full list of chunks (without content) and find out
            # the chunk groups which could use some gathering.
            for row in rows:
                if (
                    todo_length + row.length_1 > self.MAX_CHUNK_SIZE
                    or (row.last_line - todo_first_line) > self.MAX_CHUNK_LINES
                ):
                    if todo_numchunks > 1 or (force and todo_numchunks):
                        # this group is worth re-compressing
                        todo_gather_list.append((todo_first_line, todo_last_line))
                    todo_first_line = row.first_line
                    todo_length = 0
                    todo_numchunks = 0

                todo_last_line = row.last_line
                # note that we count the compressed size for efficiency reason
                # unlike to the on-the-flow chunk splitter
                todo_length += row.length_1
                totlength += row.length_1
                todo_numchunks += 1
                numchunks += 1
            rows.close()

            if totlength == 0:
                # empty log
                return 0

            if todo_numchunks > 1 or (force and todo_numchunks):
                # last chunk group
                todo_gather_list.append((todo_first_line, todo_last_line))
            for todo_first_line, todo_last_line in todo_gather_list:
                # decompress this group of chunks. Note that the content is binary bytes.
                # no need to decode anything as we are going to put in back stored as bytes anyway
                q = sa.select(tbl.c.first_line, tbl.c.last_line, tbl.c.content, tbl.c.compressed)
                q = q.where(tbl.c.logid == logid)
                q = q.where(tbl.c.first_line >= todo_first_line)
                q = q.where(tbl.c.last_line <= todo_last_line)
                q = q.order_by(tbl.c.first_line)
                rows = conn.execute(q)
                chunks: list[bytes] = []
                for row in rows:
                    compressed_chunk = self._get_compressor(row.compressed).read(row.content)
                    if compressed_chunk:
                        chunks.append(compressed_chunk)
                rows.close()

                # we remove the chunks that we are compressing
                d = tbl.delete()
                d = d.where(tbl.c.logid == logid)
                d = d.where(tbl.c.first_line >= todo_first_line)
                d = d.where(tbl.c.last_line <= todo_last_line)

                # Transaction is necessary so that readers don't see disappeared chunks
                with conn.begin_nested():
                    conn.execute(d).close()

                    # and we recompress them in one big chunk
                    chunk, compressed_id = self.thdCompressChunk(b'\n'.join(chunks))
                    conn.execute(
                        tbl.insert(),
                        {
                            "logid": logid,
                            "first_line": todo_first_line,
                            "last_line": todo_last_line,
                            "content": chunk,
                            "compressed": compressed_id,
                        },
                    ).close()

                conn.commit()

            # calculate how many bytes we saved
            q = sa.select(sa.func.sum(sa.func.length(tbl.c.content)))
            q = q.where(tbl.c.logid == logid)
            newsize = conn.execute(q).fetchone()[0]
            return totlength - newsize

        return self.db.pool.do(thdcompressLog)

    def deleteOldLogChunks(self, older_than_timestamp: int) -> defer.Deferred[int]:
        def thddeleteOldLogs(conn) -> int:
            model = self.db.model
            res = conn.execute(sa.select(sa.func.count(model.logchunks.c.logid)))
            count1 = res.fetchone()[0]
            res.close()

            # update log types older than timestamps
            # we do it first to avoid having UI discrepancy

            # N.B.: we utilize the fact that steps.id is auto-increment, thus steps.started_at
            # times are effectively sorted and we only need to find the steps.id at the upper
            # bound of steps to update.

            # SELECT steps.id from steps WHERE steps.started_at < older_than_timestamp ORDER BY
            # steps.id DESC LIMIT 1;
            res = conn.execute(
                sa.select(model.steps.c.id)
                .where(model.steps.c.started_at < older_than_timestamp)
                .order_by(model.steps.c.id.desc())
                .limit(1)
            )
            res_list = res.fetchone()
            stepid_max = None
            if res_list:
                stepid_max = res_list[0]
            res.close()

            # UPDATE logs SET logs.type = 'd' WHERE logs.stepid <= stepid_max AND type != 'd';
            if stepid_max:
                res = conn.execute(
                    model.logs.update()
                    .where(sa.and_(model.logs.c.stepid <= stepid_max, model.logs.c.type != 'd'))
                    .values(type='d')
                )
                conn.commit()
                res.close()

            # query all logs with type 'd' and delete their chunks.
            if self.db._engine.dialect.name == 'sqlite':
                # sqlite does not support delete with a join, so for this case we use a subquery,
                # which is much slower
                q = sa.select(model.logs.c.id)
                q = q.select_from(model.logs)
                q = q.where(model.logs.c.type == 'd')

                # delete their logchunks
                q = model.logchunks.delete().where(model.logchunks.c.logid.in_(q))
            else:
                q = model.logchunks.delete()
                q = q.where(model.logs.c.id == model.logchunks.c.logid)
                q = q.where(model.logs.c.type == 'd')

            res = conn.execute(q)
            conn.commit()
            res.close()
            res = conn.execute(sa.select(sa.func.count(model.logchunks.c.logid)))
            count2 = res.fetchone()[0]
            res.close()
            return count1 - count2

        return self.db.pool.do(thddeleteOldLogs)

    def _model_from_row(self, row):
        return LogModel(
            id=row.id,
            name=row.name,
            slug=row.slug,
            stepid=row.stepid,
            complete=bool(row.complete),
            num_lines=row.num_lines,
            type=row.type,
        )
