_hooks = list()


def audit(event, *args):
    global _hooks

    hooks = _hooks.copy()
    for hook in hooks:
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
