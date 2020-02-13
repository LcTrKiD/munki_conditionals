#!/usr/local/munki/python

import os
import plistlib

from sys import exit


class PPPCPConditions(object):
    """Generates a simple array of PPPCP payloads deployed via MDM."""
    def __init__(self):
        self._mdmoverrides = '/Library/Application Support/com.apple.TCC/MDMOverrides.plist'
        self._conditions_file = '/Library/Managed Installs/ConditionalItems.plist'

        self.conditions = self._process()

    def _read(self):
        result = None

        if os.path.exists(self._mdmoverrides):
            with open(self._mdmoverrides, 'rb') as _f:
                try:
                    result = plistlib.load(_f)
                except Exception:
                    exit(1)
        else:
            exit(1)

        return result

    def _process(self):
        result = {'pppcp_payloads': set()}

        _overrides = self._read()

        for _override, _payloads in _overrides.items():
            for _payload, _values in _payloads.items():
                # print(_payload)
                _identifier = _values.get('Identifier', None)

                result['pppcp_payloads'].add(_identifier)

        result['pppcp_payloads'] = list(result['pppcp_payloads'])

        return result

    def write(self):
        _data = None

        if os.path.exists(self._conditions_file):
            with open(self._conditions_file, 'rb') as _f:
                _data = plistlib.load(_f)

        if _data:
            _data['pppcp_payloads'] = self.conditions['pppcp_payloads']
        else:
            _data = self.conditions

        with open(self._conditions_file, 'wb') as _f:
            try:
                plistlib.dump(_data, _f)
                exit(0)
            except Exception:
                exit(1)


def main():
    pppcp_conditions = PPPCPConditions()
    pppcp_conditions.write()


if __name__ == '__main__':
    main()
