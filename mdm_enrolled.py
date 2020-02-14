#!/usr/local/munki/python

import os
import plistlib
import subprocess

from sys import exit


class MDMEnrolled(object):
    def __init__(self):
        self._conditions_file = '/Library/Managed Installs/ConditionalItems.plist'

        self.conditions = self._process()

    def _process(self):
        result = dict()

        _cmd = ['/usr/bin/profiles', 'status', '-type', 'enrollment']

        _subprocess = subprocess.Popen(_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _result, _error = _subprocess.communicate()

        if _subprocess.returncode == 0:
            if _result:
                _result = _result.decode('utf-8').strip().splitlines()

                for _item in _result:
                    _key = _item.lower().split(': ')[0].replace(' ', '_')
                    _value = _item.lower().split(': ')[1].replace(' ', '_').replace('(', '').replace(')', '')

                    result[_key] = _value

        return result

    def write(self):
        _data = None

        if os.path.exists(self._conditions_file):
            try:
                with open(self._conditions_file, 'rb') as _f:
                    _data = plistlib.load(_f)
            except AttributeError:
                plistlib.readPlist(self._conditions_file)

        if _data:
            _data.update(self.conditions)
        else:
            _data = dict()
            _data.update(self.conditions)

        if _data:
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
    mdm_conditions = MDMEnrolled()
    mdm_conditions.write()


if __name__ == '__main__':
    main()
