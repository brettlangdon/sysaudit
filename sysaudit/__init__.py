__all__ = ["audit", "addaudithook"]

import os
import sys

# Python 3.8+
# DEV: We could check `sys.version_info >= (3, 8)`, but if auditing ever gets
#   back ported we want to take advantage of that
std_audit = None
std_addaudithook = None
if hasattr(sys, "audit") and hasattr(sys, "addaudithook"):
    std_audit = sys.audit
    std_addaudithook = sys.addaudithook

# Try to import CPython version
csysaudit_audit = None
csysaudit_addaudithook = None
try:
    from . import _csysaudit

    csysaudit_audit = _csysaudit.audit
    csysaudit_addaudithook = _csysaudit.addaudithook
except ImportError:
    pass


# Pure-python implementation
_hooks = list()


def py_audit(event, *args):
    global _hooks

    for hook in _hooks:
        hook(event, args)


def py_addaudithook(callback):
    global _hooks

    # https://docs.python.org/3.8/library/sys.html#sys.addaudithook
    # Raise an auditing event `sys.addaudithook` with no arguments.
    # If any existing hooks raise an exception derived from RuntimeError,
    # the new hook will not be added and the exception suppressed.
    # As a result, callers cannot assume that their hook has been added
    # unless they control all existing hooks.
    try:
        audit("sys.addaudithook")
    except RuntimeError:
        return

    _hooks.append(callback)


# Choose the best implementation
# DEV: We still import/create all of them
#      so we can easily access each implementation
#      for testing
SYSAUDIT_IMPL = os.getenv("SYSAUDIT_IMPL")
if SYSAUDIT_IMPL:
    if SYSAUDIT_IMPL == "stdlib":
        audit = std_audit
        addaudithook = std_addaudithook
    elif SYSAUDIT_IMPL == "csysaudit":
        audit = csysaudit_audit
        addaudithook = csysaudit_addaudithook
    elif SYSAUDIT_IMPL == "pysysaudit":
        audit = py_audit
        addaudithook = py_addaudithook
    else:
        raise ValueError(
            "SYSAUDIT_IMPL must be one of ('stdlib', 'csysaudit', 'pysysaudit')"
        )
else:
    if std_audit and std_addaudithook:
        audit = std_audit
        addaudithook = std_addaudithook
    elif csysaudit_audit and csysaudit_addaudithook:
        audit = csysaudit_audit
        addaudithook = csysaudit_addaudithook
    else:
        audit = py_audit
        addaudithook = py_addaudithook
