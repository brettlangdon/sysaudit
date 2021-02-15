sysaudit
========
.. image:: https://readthedocs.org/projects/sysaudit/badge/?version=latest
  :target: https://sysaudit.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

.. image: https://github.com/brettlangdon/sysaudit/workflows/Build/badge.svg?branch=main&event=push
  :target: https://github.com/brettlangdon/sysaudit/actions?query=branch%3Amain+workflow%3ABuild+event%3Apush
  :alt: Build status

Backport module of `sys.audit <https://docs.python.org/3.8/library/sys.html#sys.audit>`_
and `sys.addaudithook <https://docs.python.org/3.8/library/sys.html#sys.addaudithook>`_
from Python 3.8.

**Note:** This module does *not* backport any of the built-in
`audit events <https://docs.python.org/3.8/library/audit_events.html#audit-events>`_.


Installation
------------

.. code-block:: bash

    pip install sysaudit

Quick Usage
-----------

`sysaudit` can be used as a drop-in replacement for `sys.audit` and `sys.addaudithook`.

.. code-block:: python

  import sysaudit

  def hook(event, args):
      print("Event:", event, args)

  sysaudit.addaudithook(hook)

  sysaudit.audit("event_name", 1, 2, dict(key="value"))
  # Event: event_name (1, 2, {'key': 'value'})
