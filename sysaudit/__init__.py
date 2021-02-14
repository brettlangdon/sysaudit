__all__ = ["audit", "addaudithook", "subscribe", "Span"]

import collections
import sys

# Python 3.8+
# DEV: We could check `sys.version_info >= (3, 8)`, but if auditing ever gets
#   back ported we want to take advantage of that
if hasattr(sys, "audit") and hasattr(sys, "addaudithook"):
    audit = sys.audit
    addaudithook = sys.addaudithook
else:
    try:
        from ._csysaudit import audit, addaudithook
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


_subscriptions = collections.defaultdict(list)
_subscription_hook_active = False


def _subscription_hook(event, args):
    if event in _subscriptions:
        # Grab a copy of hooks so we don't need to lock here
        for hook in _subscriptions[event][:]:
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

    def end(self, data=None):
        if not self.ended:
            self.message("end", data)
            self.ended = True

    def annotate(self, data):
        self.message("annotate", data)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end(data=dict(exc_type=exc_type, exc_val=exc_val, exc_tb=exc_tb))

    def __str__(self):
        return "{0}(name={1!r}, id={2!r}, data={3!r})".format(
            self.__class__.__name__,
            self.name,
            self.id,
            self.data,
        )
