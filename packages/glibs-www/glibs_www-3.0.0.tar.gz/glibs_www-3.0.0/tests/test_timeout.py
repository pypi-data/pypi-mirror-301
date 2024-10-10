import gevent
import pytest
import sys
import time
import webtest

from glibs.www import timeout


class AnotherException(Exception):
    pass


def pyramid_app():
    pyramid = pytest.importorskip("pyramid")

    import pyramid.config

    config = pyramid.config.Configurator()
    config.registry.settings["gevent_timeout"] = "1"
    config.registry.settings["custom_timeout_by_endpoint"] = {
        "/test/custom/timeout/timeout": 1
    }

    def view(request):
        if request.matchdict.get("op") == "timeout":
            gevent.sleep(40)
        elif request.matchdict.get("op") == "exception":
            raise AnotherException
        elif request.matchdict.get("op") == "python-timeout":
            now = time.time()
            while time.time() - now < 1.1:
                pass
        return "ok"

    def view_custom_timeout(request):
        if request.matchdict.get("op") == "timeout":
            gevent.sleep(40)
        return "ok"

    def view_health_check(_request):
        gevent.sleep(40)
        pass

    config.add_route("test route", pattern="/test/{op}")
    config.add_route("test custom timeout route", pattern="/test/custom/timeout/{op}")
    config.add_route("test health check", pattern="/health-check")
    config.add_view(view, route_name="test route", renderer="string")
    config.add_view(
        view_custom_timeout, route_name="test custom timeout route", renderer="string"
    )
    config.add_view(
        view_health_check, route_name="test health check", renderer="string"
    )

    timeout.bind_pyramid(config)

    return webtest.TestApp(config.make_wsgi_app())


def flask_app():
    flask = pytest.importorskip("flask")

    app = flask.Flask(__name__)
    app.config["gevent_timeout"] = "1"
    app.testing = True

    @app.route("/test/<op>")
    def view(op):
        if op == "timeout":
            gevent.sleep(40)
        elif op == "exception":
            raise AnotherException()
        elif op == "python-timeout":
            now = time.time()
            while time.time() - now < 1.1:
                pass
        return "ok"

    @app.route("/test/custom/timeout/<op>")
    def view_custom_timeout(op):
        if op == "timeout":
            gevent.sleep(40)
        return "ok"

    timeout.bind_flask(app)

    return webtest.TestApp(app)


@pytest.fixture(params=[(flask_app, "flask"), (pyramid_app, "pyramid")])
def app(request):
    app_callable, framework_name = request.param
    return {"app": app_callable(), "framework": framework_name}


def test_ok(app):
    response = app["app"].get("/test/ok")
    assert response.status_code == 200


def test_ok_with_custom_timeout(app):
    response = app["app"].get("/test/custom/timeout/ok")
    assert response.status_code == 200


def test_timeout_on_gevent(app):
    expected_exception = (
        timeout.DeadlineExceededError
        if app["framework"] == "flask"
        else webtest.app.AppError
    )
    with pytest.raises(expected_exception):
        app["app"].get("/test/timeout")


def test_timeout_on_custom_timeout(app):
    expected_exception = (
        timeout.DeadlineExceededError
        if app["framework"] == "flask"
        else webtest.app.AppError
    )
    with pytest.raises(expected_exception):
        app["app"].get("/test/custom/timeout/timeout")


def test_timeout_on_python(app):
    expected_exception = (
        timeout.DeadlineExceededError
        if app["framework"] == "flask"
        else webtest.app.AppError
    )
    with pytest.raises(expected_exception):
        app["app"].get("/test/python-timeout")


def test_timeout_on_python_and_no_module_gevent(app, monkeypatch):
    monkeypatch.setitem(sys.modules, "gevent", None)
    expected_exception = (
        timeout.DeadlineExceededError
        if app["framework"] == "flask"
        else webtest.app.AppError
    )
    with pytest.raises(expected_exception):
        app["app"].get("/test/python-timeout")


def test_keeps_exception(app):
    with pytest.raises(AnotherException):
        app["app"].get("/test/exception")


def test_pyramid_tween_returns_504_response_if_timed_out():
    app = pyramid_app()
    with pytest.raises(webtest.app.AppError) as ctx_manager:
        app.get("/test/timeout")

    assert "Bad response: 504 Gateway Timeout" in str(ctx_manager.value)


def test_pyramid_tween_returns_500_response_if_health_check_endpoint_timed_out():
    app = pyramid_app()
    with pytest.raises(webtest.app.AppError) as ctx_manager:
        app.get("/health-check")

    assert "Bad response: 500 Internal Server Error" in str(ctx_manager.value)
