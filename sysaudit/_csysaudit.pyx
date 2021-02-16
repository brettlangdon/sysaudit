cdef list hooks = []
cdef int has_hooks = 0


cdef void _audit(str event, tuple args) except *:
    global hooks
    for hook in hooks:
        hook(event, args)


def audit(event, *args):
    global has_hooks

    if has_hooks == 0:
        return
    _audit(event, args)


cpdef void addaudithook(callback) except *:
    global hooks
    global has_hooks

    # https://docs.python.org/3.8/library/sys.html#sys.addaudithook
    # Raise an auditing event `sys.addaudithook` with no arguments.
    # If any existing hooks raise an exception derived from RuntimeError,
    # the new hook will not be added and the exception suppressed.
    # As a result, callers cannot assume that their hook has been added
    # unless they control all existing hooks.
    try:
        _audit("sys.addaudithook", tuple())
    except RuntimeError:
        return

    has_hooks = 1
    hooks.append(callback)
