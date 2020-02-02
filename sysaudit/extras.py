__all__ = ["audithook", "auditfunc", "auditmanager", "auditwsgi"]

import contextlib
import functools
from .audit import audit, addaudithook


def audithook(*events):
    def dec(func):
        def hook(event, args):
            if event in events:
                func(*args)

        addaudithook(hook)
        return func

    return dec


def auditfunc(event_prefix):
    started_event = "{}.started".format(event_prefix)
    finished_event = "{}.finished".format(event_prefix)

    def dec(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ret = None
            exc = None
            try:
                audit(started_event, args, kwargs)

                ret = func(*args, **kwargs)
                return ret
            except Exception as e:
                exc = e
                raise
            finally:
                audit(finished_event, ret, exc)

        return wrapper

    return dec


@contextlib.contextmanager
def auditmanager(event_prefix, *args):
    started_event = "{}.started".format(event_prefix)
    finished_event = "{}.finished".format(event_prefix)

    audit(started_event, *args)
    exc = None
    try:
        yield
    except Exception as e:
        exc = e
        raise
    finally:
        audit(finished_event, exc)


def auditwsgi(app, event_prefix="wsgi"):
    request_event = "{}.request.started".format(event_prefix)
    finished_event = "{}.request.finished".format(event_prefix)
    start_response_started_event = "{}.start_response.started".format(event_prefix)
    start_response_finished_event = "{}.start_response.finished".format(event_prefix)

    def wsgi(environ, start_response):
        audit(request_event, environ, start_response)

        def audit_start_response(status, headers):
            audit(start_response_started_event, status, headers)
            ret = None
            exc = None
            try:
                ret = start_response(status, headers)
                return ret
            except Exception as e:
                exc = e
                raise
            finally:
                audit(start_response_finished_event, ret, exc)

        ret = None
        exc = None
        try:
            ret = app(environ, audit_start_response)
            return ret
        except Exception as e:
            exc = e
            raise
        finally:
            audit(finished_event, ret, exc)

    return wsgi
