sysaudit
========

Backport module of [sys.audit](https://docs.python.org/3.8/library/sys.html#sys.audit)
and [sys.addaudithook](https://docs.python.org/3.8/library/sys.html#sys.addaudithook)
from Python 3.8.

**Note:** This module does _not_ backport any of the built-in
[audit events](https://docs.python.org/3.8/library/audit_events.html#audit-events).


## Installation

```
pip install sysaudit
```

## Usage

`sysaudit` can be used as a drop-in replacement for `sys.audit` and `sys.addaudithook`.

``` python
import sysaudit

def hook(event, args):
    print("Event:", event, args)
    
sysaudit.addaudithook(hook)

sysaudit.audit("event_name", 1, 2, dict(key="value"))
# Event: event_name (1, 2, {'key': 'value'})
```
