import mock
import pytest

import sysaudit


def assert_span_message(span, call_args, type, data=None):
    (args,) = call_args
    (message,) = args

    assert isinstance(message, sysaudit.Span.Message)
    assert message.span == span
    assert message.type == type
    assert message.data == data


def assert_start_message(span, call_args, data=None):
    assert_span_message(span, call_args, "start", data=data)


def assert_end_message(span, call_args, data=None):
    assert_span_message(span, call_args, "end", data=data)


def assert_annotate_message(span, call_args, data=None):
    assert_span_message(span, call_args, "annotate", data=data)


def test_properties():
    # Name only
    span = sysaudit.Span("span.name")
    assert span.started is False
    assert span.ended is False
    assert span.data is None
    assert span.name == "span.name"
    assert span.id == id(span)

    # Name and data
    span = sysaudit.Span("span.name", data="some-data")
    assert span.started is False
    assert span.ended is False
    assert span.data == "some-data"
    assert span.name == "span.name"
    assert span.id == id(span)


def test_started_ended():
    span = sysaudit.Span("span.name")

    span.start()
    assert span.started is True
    assert span.ended is False

    span.end()
    assert span.started is True
    assert span.ended is True


def test_started_ended_contextmanager():
    span = sysaudit.Span("span.name")
    with span:
        assert span.started is True
        assert span.ended is False

    assert span.started is True
    assert span.ended is True


def test_lifecycle_events():
    hook = mock.Mock()
    sysaudit.subscribe("span.name", hook)

    span = sysaudit.Span("span.name")
    hook.assert_not_called()

    span.start()
    assert hook.call_count == 1
    assert_start_message(span, hook.call_args[0])

    # Call a second time
    span.start()
    # We did not emit a second start message
    assert hook.call_count == 1

    span.end()
    assert hook.call_count == 2
    assert_end_message(span, hook.call_args[0])

    # Call a second time
    span.end()
    # We did not emit a second end message
    assert hook.call_count == 2


def test_lifecycle_events_contextmanager():
    hook = mock.Mock()
    sysaudit.subscribe("span.name", hook)

    with sysaudit.Span("span.name") as span:
        assert hook.call_count == 1
        assert_start_message(span, hook.call_args[0])

    assert hook.call_count == 2
    assert_end_message(
        span, hook.call_args[0], data=dict(exc_tb=None, exc_type=None, exc_val=None)
    )


def test_lifecycle_events_data():
    hook = mock.Mock()
    sysaudit.subscribe("span.name", hook)

    span = sysaudit.Span("span.name")

    span.start("start-data")
    assert hook.call_count == 1
    assert_start_message(span, hook.call_args[0], data="start-data")

    span.end("end-data")
    assert hook.call_count == 2
    assert_end_message(span, hook.call_args[0], data="end-data")


def test_end_before_start():
    span = sysaudit.Span("span.name")

    with pytest.raises(RuntimeError):
        span.end()


def test_custom_message():
    hook = mock.Mock()
    sysaudit.subscribe("span.name", hook)

    span = sysaudit.Span("span.name")
    span.message("custom", "message")

    assert hook.call_count == 1
    assert_span_message(span, hook.call_args[0], type="custom", data="message")


def test_annotate_message():
    hook = mock.Mock()
    sysaudit.subscribe("span.name", hook)

    span = sysaudit.Span("span.name")
    span.annotate("extra-data")

    assert hook.call_count == 1
    assert_annotate_message(span, hook.call_args[0], data="extra-data")
