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
                exit(1)

    def disconnect(self, db):
        try:
            self.connection.execute("")
            try:
                self.connection.close()
                try:
                    self.connection.execute("")
                except Exception:
                    exit(1)
            except Exception:
                exit(1)
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
            _mdm_query = _sqldb.query('SELECT team_id, bundle_id, allowed FROM kext_policy_mdm', fetch=True)
            _user_query = _sqldb.query('SELECT team_id, bundle_id, allowed FROM kext_policy', fetch=True)

            if _mdm_query:
                for team_id, bundle_id, allowed in _mdm_query:
                    if allowed == 1:
                        if team_id:
                            result['kext_teams'].add(team_id)

                        if bundle_id:
                            result['kext_bundles'].add(bundle_id)

            if _user_query:
                for team_id, bundle_id, allowed in _user_query:
                    if allowed == 1:
                        if team_id:
                            result['kext_teams'].add(team_id)

                        if bundle_id:
                            result['kext_bundles'].add(bundle_id)

            result['kext_teams'] = list(result['kext_teams'])
            result['kext_bundles'] = list(result['kext_bundles'])
        else:
            result['kext_teams'] = list()
            result['kext_bundles'] = list()

        return result

    def write(self):
        _data = None

        if os.path.exists(self._conditions_file):
            try:
                with open(self._conditions_file, 'rb') as _f:
                    _data = plistlib.load(_f)
            except AttributeError:
                _data = plistlib.readPlist(self._conditions_file)

        if not _data:
            _data = dict()

        _data.update(self.conditions)

        with open(self._conditions_file, 'wb') as _f:
            try:
                plistlib.dump(_data, _f)
                exit(0)
            except AttributeError:
                plistlib.writePlist(_data, self._conditions_file)
                exit(0)
            except Exception:
                exit(1)


def main():
    kext_conditions = KextPolicy()
    kext_conditions.write()


if __name__ == '__main__':
    main()
