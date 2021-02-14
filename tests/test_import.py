import sys

import sysaudit


def test_module():
    if sys.version_info >= (3, 8, 0):
        assert sysaudit.audit == sys.audit
        assert sysaudit.addaudithook == sys.addaudithook
    else:
        assert sysaudit.audit == sysaudit._csysaudit.audit
        assert sysaudit.addaudithook == sysaudit._csysaudit.addaudithook
