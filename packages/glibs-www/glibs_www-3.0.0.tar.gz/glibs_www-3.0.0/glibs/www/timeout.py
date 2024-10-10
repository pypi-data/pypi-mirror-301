"""
This timeout module is useful on deployment environments that implement a timeout on
requests. Usually this timeout is implemented on the HTTP layer, thus we have no
information on runtime (for logging, metrics, etc.) that the request timed out.

What this module does is raise a `DeadlineExceededError` exception so this error can
show up in error aggregators.

For pyramid applications, the `DeadlineExceededError` is not raised, since according to the
documentation, tweens are required to return a Response. Instead, a status code 500 response is
returned for `/health-check` route requests, and a status code 504 response for other endpoints.
"""

import functools
import time

__all__ = ["DeadlineExceededError", "bind_pyramid", "bind_flask"]


class DeadlineExceededError(Exception):
    pass


class _FakeTimer:
    def start(self):
        pass

    def close(self):
        pass


def _timeout(seconds):
    try:
        import gevent

        return gevent.Timeout(seconds, DeadlineExceededError)
    except ImportError:
        return _FakeTimer()


def bind_flask(app):
    timeout_seconds = int(app.config.get("gevent_timeout", "30"))

    def wrap_dispatch_request(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):  # pragma: no cover
            timeout = _timeout(timeout_seconds)
            timeout.start()
            start_time = time.time()
            try:
                result = f(*args, **kwargs)
                if time.time() - start_time > timeout_seconds:
                    raise DeadlineExceededError()
                return result
            finally:
                timeout.close()

        return wrapper

    app.dispatch_request = wrap_dispatch_request(app.dispatch_request)


def bind_pyramid(config):
    config.add_tween("glibs.www.timeout.pyramid_tween")


def pyramid_tween(handler, registry):
    from pyramid.response import Response

    custom_timeout_by_endpoint = registry.settings.get("custom_timeout_by_endpoint", {})
    default_timeout_in_seconds = int(registry.settings.get("gevent_timeout", "30"))

    def request_timeout(request):
        if request.path in custom_timeout_by_endpoint.keys():
            timeout = _timeout(int(custom_timeout_by_endpoint[request.path]))
            max_time_to_wait = custom_timeout_by_endpoint[request.path]
        else:
            timeout = _timeout(default_timeout_in_seconds)
            max_time_to_wait = default_timeout_in_seconds
        timeout.start()
        start_time = time.time()
        try:
            result = handler(request)
            if time.time() - start_time > max_time_to_wait:
                raise DeadlineExceededError()
            return result
        except DeadlineExceededError:
            # Return a response with status code 500 for standardized health-check routes, which is
            # the status code used by AWS to determine when an instance or container is unhealthy
            if request.path.startswith("/health-check"):
                return Response(status=500)
            return Response(status=504)
        finally:
            timeout.close()

    return request_timeout
