import sys

import sysaudit


def test_module():  # type: () -> None
    assert sysaudit.audit is not None
    assert sysaudit.addaudithook is not None

    if sys.version_info >= (3, 8, 0):
        assert sysaudit.std_audit == sys.audit
        assert sysaudit.std_addaudithook == sys.addaudithook
        assert sysaudit.audit == sys.audit  # type: ignore [attr-defined]
        assert sysaudit.addaudithook == sys.addaudithook  # type: ignore [attr-defined]
    else:
        assert sysaudit.audit == sysaudit.csysaudit_audit
        assert sysaudit.addaudithook == sysaudit.csysaudit_addaudithook

    assert sysaudit.py_audit is not None
    assert sysaudit.py_addaudithook is not None
