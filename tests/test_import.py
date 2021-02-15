import sys

import sysaudit


def test_module():  # type: () -> None
    if sys.version_info >= (3, 8, 0):
        assert sysaudit.audit == sys.audit  # type: ignore [attr-defined]
        assert sysaudit.addaudithook == sys.addaudithook  # type: ignore [attr-defined]
    else:
        assert sysaudit.audit == sysaudit._csysaudit.audit
        assert sysaudit.addaudithook == sysaudit._csysaudit.addaudithook
