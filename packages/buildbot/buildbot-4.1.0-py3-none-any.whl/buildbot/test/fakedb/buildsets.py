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

import json
from typing import TYPE_CHECKING

from twisted.internet import defer

from buildbot.db import buildsets
from buildbot.test.fakedb.base import FakeDBComponent
from buildbot.test.fakedb.buildrequests import BuildRequest
from buildbot.test.fakedb.row import Row
from buildbot.util import datetime2epoch
from buildbot.util import epoch2datetime

if TYPE_CHECKING:
    from buildbot.db.sourcestamps import SourceStampModel


class Buildset(Row):
    table = "buildsets"
    foreignKeys = ('rebuilt_buildid',)

    id_column = 'id'

    def __init__(
        self,
        id=None,
        external_idstring='extid',
        reason='because',
        submitted_at=12345678,
        complete=0,
        complete_at=None,
        results=-1,
        rebuilt_buildid=None,
        parent_buildid=None,
        parent_relationship=None,
    ):
        super().__init__(
            id=id,
            external_idstring=external_idstring,
            reason=reason,
            submitted_at=submitted_at,
            complete=complete,
            complete_at=complete_at,
            results=results,
            rebuilt_buildid=rebuilt_buildid,
            parent_buildid=parent_buildid,
            parent_relationship=parent_relationship,
        )


class BuildsetProperty(Row):
    table = "buildset_properties"

    foreignKeys = ('buildsetid',)
    required_columns = ('buildsetid',)

    def __init__(self, buildsetid=None, property_name='prop', property_value='[22, "fakedb"]'):
        super().__init__(
            buildsetid=buildsetid, property_name=property_name, property_value=property_value
        )


class BuildsetSourceStamp(Row):
    table = "buildset_sourcestamps"

    foreignKeys = ('buildsetid', 'sourcestampid')
    required_columns = (
        'buildsetid',
        'sourcestampid',
    )
    id_column = 'id'

    def __init__(self, id=None, buildsetid=None, sourcestampid=None):
        super().__init__(id=id, buildsetid=buildsetid, sourcestampid=sourcestampid)


class FakeBuildsetsComponent(FakeDBComponent):
    def setUp(self):
        self.buildsets = {}
        self.completed_bsids = set()
        self.buildset_sourcestamps = {}

    def insert_test_data(self, rows):
        for row in rows:
            if isinstance(row, Buildset):
                bs = self.buildsets[row.id] = row.values.copy()
                bs['properties'] = {}

        for row in rows:
            if isinstance(row, BuildsetProperty):
                assert row.buildsetid in self.buildsets
                n = row.property_name
                v, src = tuple(json.loads(row.property_value))
                self.buildsets[row.buildsetid]['properties'][n] = (v, src)

        for row in rows:
            if isinstance(row, BuildsetSourceStamp):
                assert row.buildsetid in self.buildsets
                self.buildset_sourcestamps.setdefault(row.buildsetid, []).append(row.sourcestampid)

    # component methods

    def _newBsid(self):
        bsid = 200
        while bsid in self.buildsets:
            bsid += 1
        return bsid

    @defer.inlineCallbacks
    def addBuildset(
        self,
        sourcestamps,
        reason,
        properties,
        builderids,
        waited_for,
        external_idstring=None,
        submitted_at=None,
        rebuilt_buildid=None,
        parent_buildid=None,
        parent_relationship=None,
        priority=0,
    ):
        # We've gotten this wrong a couple times.
        assert isinstance(waited_for, bool), f'waited_for should be boolean: {waited_for!r}'

        # calculate submitted at
        if submitted_at is not None:
            submitted_at = datetime2epoch(submitted_at)
        else:
            submitted_at = int(self.reactor.seconds())

        bsid = self._newBsid()
        br_rows = []
        for builderid in builderids:
            br_rows.append(
                BuildRequest(
                    buildsetid=bsid,
                    builderid=builderid,
                    waited_for=waited_for,
                    submitted_at=submitted_at,
                )
            )

        self.db.buildrequests.insert_test_data(br_rows)

        # make up a row and keep its dictionary, with the properties tacked on
        bsrow = Buildset(
            id=bsid,
            reason=reason,
            external_idstring=external_idstring,
            submitted_at=submitted_at,
            rebuilt_buildid=rebuilt_buildid,
            parent_buildid=parent_buildid,
            parent_relationship=parent_relationship,
        )

        self.buildsets[bsid] = bsrow.values.copy()
        self.buildsets[bsid]['properties'] = properties

        # add sourcestamps
        ssids = []
        for ss in sourcestamps:
            if not isinstance(ss, int):
                ss = yield self.db.sourcestamps.findSourceStampId(**ss)
            ssids.append(ss)
        self.buildset_sourcestamps[bsid] = ssids

        return (bsid, {br.builderid: br.id for br in br_rows})

    def completeBuildset(self, bsid, results, complete_at=None):
        if bsid not in self.buildsets or self.buildsets[bsid]['complete']:
            raise buildsets.AlreadyCompleteError()

        if complete_at is not None:
            complete_at = datetime2epoch(complete_at)
        else:
            complete_at = int(self.reactor.seconds())

        self.buildsets[bsid]['results'] = results
        self.buildsets[bsid]['complete'] = 1
        self.buildsets[bsid]['complete_at'] = complete_at
        return defer.succeed(None)

    def getBuildset(self, bsid: int) -> defer.Deferred[buildsets.BuildSetModel | None]:
        if bsid not in self.buildsets:
            return defer.succeed(None)
        row = self.buildsets[bsid]
        return defer.succeed(self._model_from_row(row))

    def getBuildsets(
        self, complete: bool | None = None, resultSpec=None
    ) -> defer.Deferred[list[buildsets.BuildSetModel]]:
        rv = []
        for bs in self.buildsets.values():
            if complete is not None:
                if complete and bs['complete']:
                    rv.append(bs)
                elif not complete and not bs['complete']:
                    rv.append(bs)
            else:
                rv.append(bs)
        if resultSpec is not None:
            rv = self.applyResultSpec(rv, resultSpec)

        rv = [self._model_from_row(bs) for bs in rv]
        return defer.succeed(rv)

    @defer.inlineCallbacks
    def getRecentBuildsets(self, count=None, branch=None, repository=None, complete=None):
        if not count:
            return []
        rv = []
        for bs in (yield self.getBuildsets(complete=complete)):
            if branch or repository:
                ok = True
                if not bs.sourcestamps:
                    # no sourcestamps -> no match
                    ok = False
                for ssid in bs.sourcestamps:
                    ss: SourceStampModel = yield self.db.sourcestamps.getSourceStamp(ssid)
                    if branch and ss.branch != branch:
                        ok = False
                    if repository and ss.repository != repository:
                        ok = False
            else:
                ok = True

            if ok:
                rv.append(bs)

        rv.sort(key=lambda bs: -bs.bsid)

        return list(reversed(rv[:count]))

    def _model_from_row(self, row) -> buildsets.BuildSetModel:
        return buildsets.BuildSetModel(
            bsid=row['id'],
            external_idstring=row['external_idstring'],
            reason=row['reason'],
            submitted_at=epoch2datetime(row['submitted_at']),
            complete=bool(row['complete']),
            complete_at=epoch2datetime(row['complete_at']),
            results=row['results'],
            parent_buildid=row['parent_buildid'],
            parent_relationship=row['parent_relationship'],
            rebuilt_buildid=row['rebuilt_buildid'],
            sourcestamps=self.buildset_sourcestamps.get(row['id'], []),
        )

    def getBuildsetProperties(self, key, no_cache=False):
        if key in self.buildsets:
            return defer.succeed(self.buildsets[key]['properties'])
        return defer.succeed({})

    # fake methods

    def fakeBuildsetCompletion(self, bsid, result):
        assert bsid in self.buildsets
        self.buildsets[bsid]['results'] = result
        self.completed_bsids.add(bsid)

    # assertions

    def assertBuildsetCompletion(self, bsid, complete):
        """Assert that the completion state of buildset BSID is COMPLETE"""
        actual = self.buildsets[bsid]['complete']
        self.t.assertTrue((actual and complete) or (not actual and not complete))

    def assertBuildset(self, bsid=None, expected_buildset=None):
        """Assert that the given buildset looks as expected; the ssid parameter
        of the buildset is omitted.  Properties are converted with asList and
        sorted.  Attributes complete, complete_at, submitted_at, results, and parent_*
        are ignored if not specified."""
        self.t.assertIn(bsid, self.buildsets)
        buildset = self.buildsets[bsid].copy()
        del buildset['id']

        # clear out some columns if the caller doesn't care
        columns = [
            'complete',
            'complete_at',
            'submitted_at',
            'results',
            'parent_buildid',
            'parent_relationship',
        ]
        for col in columns:
            if col not in expected_buildset:
                del buildset[col]

        if buildset['properties']:
            buildset['properties'] = sorted(buildset['properties'].items())

        self.t.assertEqual(buildset, expected_buildset)
        return bsid
