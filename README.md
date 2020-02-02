sysaudit
========

Backport module of [sys.audit](https://docs.python.org/3.8/library/sys.html#sys.audit)
and [sys.addaudithook](https://docs.python.org/3.8/library/sys.html#sys.addaudithook)
from Python 3.8.

This module provides the audit hooking mechanisms and some helpers to help
library developers usage of `sys.audit`.

**Note:** This module does _not_ backport any of the built-in
[audit events](https://docs.python.org/3.8/library/audit_events.html#audit-events).
