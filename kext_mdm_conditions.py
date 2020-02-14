#!/usr/local/munki/python

import os
import plistlib
import sqlite3

from sys import exit


class SQLite():
    connection = ''
    c = ''

    def connect(self, db):
        try:
            self.connection.execute("")
        except Exception:
            try:
                self.connection = sqlite3.connect(db)
                self.c = self.connection.cursor()
            except Exception:
                raise
                exit(1)

    def disconnect(self, db):
        try:
            self.connection.execute("")
            try:
                self.connection.close()
                try:
                    self.connection.execute("")
                except Exception:
                    raise
            except Exception:
                raise
        except Exception:
            pass

    def query(self, query_string, fetch=False):
        try:
            self.c.execute(query_string)
            if not fetch:
                self.c.execute(query_string)
            else:
                self.c.execute(query_string)
                return self.c.fetchall()
        except Exception:
            raise


class KextPolicy(object):
    def __init__(self):
        self._kextpolicy = '/var/db/SystemPolicyConfiguration/KextPolicy'
        self._conditions_file = '/Library/Managed Installs/ConditionalItems.plist'

        self.conditions = self._process()

    def _process(self):
        result = dict()

        if os.path.exists(self._kextpolicy):
            result['kext_teams'] = set()
            result['kext_bundles'] = set()

            _sqldb = SQLite()

            _sqldb.connect(self._kextpolicy)
            _query = _sqldb.query('SELECT team_id, bundle_id, allowed FROM kext_policy_mdm', fetch=True)

            if _query:
                for team_id, bundle_id, allowed in _query:
                    if allowed == 1:
                        if team_id:
                            result['kext_mdm_teams'].add(team_id)

                        if bundle_id:
                            result['kext_mdm_bundles'].add(bundle_id)

            _sqldb.disconnect(self._kextpolicy)

            result['kext_mdm_teams'] = list(result['kext_mdm_teams'])
            result['kext_mdm_bundles'] = list(result['kext_mdm_bundles'])
        else:
            exit(1)

        return result

    def write(self):
        _data = None

        if os.path.exists(self._conditions_file):
            with open(self._conditions_file, 'rb') as _f:
                _data = plistlib.load(_f)

        if _data:
            _data['kext_mdm_teams'] = self.conditions.get('kext_mdm_teams', None)
            _data['kext_mdm_bundles'] = self.conditions.get('kext_mdm_bundles', None)
        else:
            _data = self.conditions

        with open(self._conditions_file, 'wb') as _f:
            try:
                plistlib.dump(_data, _f)
                exit(0)
            except Exception:
                exit(1)


kext_conditions = KextPolicy()
kext_conditions.write()
