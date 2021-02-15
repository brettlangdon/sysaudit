import mock

import sysaudit


def test_basic():
    test_hook = mock.Mock()
    event_hook = mock.Mock()

    sysaudit.subscribe("test", test_hook)
    sysaudit.subscribe("event", event_hook)

    assert sysaudit._subscriptions == dict(test=[test_hook], event=[event_hook])

    sysaudit.audit("test", 1)
    sysaudit.audit("test", 2)
    sysaudit.audit("event", 3)
    sysaudit.audit("event", 4)
    sysaudit.audit("event", 5)

    assert test_hook.mock_calls == [
        mock.call((1,)),
        mock.call((2,)),
    ]
    assert event_hook.mock_calls == [
        mock.call((3,)),
        mock.call((4,)),
        mock.call((5,)),
    ]


def test_multiple_hooks():
    test_hook_1 = mock.Mock()
    test_hook_2 = mock.Mock()
    test_hook_3 = mock.Mock()

    sysaudit.subscribe("test", test_hook_1)
    sysaudit.subscribe("test", test_hook_2)
    sysaudit.subscribe("test", test_hook_3)

    sysaudit.audit("test", 1)

    test_hook_1.assert_called_once_with(((1,)))
    test_hook_2.assert_called_once_with(((1,)))
    test_hook_3.assert_called_once_with(((1,)))
