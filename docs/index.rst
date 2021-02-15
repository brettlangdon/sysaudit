.. toctree::
   :maxdepth: 3

.. include:: ../README.rst

API
---

.. py:module:: sysaudit

.. py:function:: audit(event: str, *args: typing.Any) -> None

   Passes the event to any audit hooks that are attached via :py:func:`addaudithook`.

   :param str event:
   :param typing.Any \*args:
   :rtype: None

   .. code-block:: python

     sysaudit.audit("event_name", "any", "extra", dict(args="here"))

.. py:function:: addaudithook(hook: typing.Callable[[str, typing.Tuple[typing.Any, ...], None]]) -> None

   Adds a new audit hook callback.

   :param callable hook: Function to call with every event from :py:func:`audit`
   :rtype: None

   .. code-block:: python

     def hook(event: str, args: typing.Tuple[typing.Any, ...]) -> None:
         print("Event:", event, "Args:", args)


     sysaudit.addaudithook(hook)

     sysaudit.audit("event_name", 1, 2, 3)
     # Event: event_name Args: (1, 2, 3)


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
