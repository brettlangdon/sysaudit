__all__ = ["audit", "addaudithook", "subscribe", "Span"]

import collections
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

# Try to import Cython version
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

    if callback not in _hooks:
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


# Subscriptions
_subscriptions = collections.defaultdict(list)
_subscription_hook_active = False


def _subscription_hook(event, args):
    if event in _subscriptions:
        for hook in _subscriptions[event]:
            hook(args)


def subscribe(event, hook):
    global _subscriptions
    global _subscription_hook_active

    if not _subscription_hook_active:
        addaudithook(_subscription_hook)
        _subscription_hook_active = True

    if hook not in _subscriptions[event]:
        _subscriptions[event].append(hook)


class Span:
    __slots__ = ("name", "started", "ended", "data")

    class Message:
        __slots__ = ("type", "span", "data")

        def __init__(self, type, span, data=None):
            self.type = type
            self.span = span
            self.data = data

        def __str__(self):
            return "{0}(type={1!r}, span={2}, data={3!r})".format(
                self.__class__.__name__, self.type, self.span, self.data
            )

    def __init__(self, name, data=None):
        self.name = name
        self.started = False
        self.ended = False
        self.data = data

    @property
    def id(self):
        return id(self)

    def message(self, type, data=None):
        audit(self.name, self.Message(type, self, data))

    def start(self, data=None):
        if not self.started:
            self.message("start", data)
            self.started = True

        # Return `self` so we can explicitly call `start` with data in a context manager:
        #     with sysaudit.Span("my.event").start(dict(start_only="data")) as span:
        #         pass
        return self

    def end(self, data=None):
        if not self.started:
            raise RuntimeError(
                "Attempting to end span {} before it was started".format(self)
            )
        if not self.ended:
            self.message("end", data)
            self.ended = True

    def annotate(self, data):
        self.message("annotate", data)

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end(data=dict(exc_type=exc_type, exc_val=exc_val, exc_tb=exc_tb))

    def __str__(self):
        return "{0}(name={1!r}, id={2!r}, data={3!r})".format(
            self.__class__.__name__,
            self.name,
            self.id,
            self.data,
        )
