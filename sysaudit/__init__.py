__all__ = ["audit", "addaudithook"]

import sys

# Python 3.8+
# DEV: We could check `sys.version_info >= (3, 8)`, but if auditing ever gets
#   back ported we want to take advantage of that
if hasattr(sys, "audit") and hasattr(sys, "addaudithook"):
    audit = sys.audit
    addaudithook = sys.addaudithook
else:
    try:
        from .csysaudit import audit, addaudithook
    except ImportError:
        _hooks = list()

        def audit(event, *args):
            global _hooks
            # Grab a copy of hooks so we don't need to lock here
            for hook in _hooks[:]:
                hook(event, args)

        def addaudithook(callback):
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

            if callback not in _hooks:
                _hooks.append(callback)
