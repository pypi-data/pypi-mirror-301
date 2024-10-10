# coding: utf-8
import json
import logging
import pytest
import re
import webtest

from glibs.www import request_logger


class ViewError(Exception):
    pass


def flask_app(get_user_id=lambda: "john"):
    flask = pytest.importorskip("flask")
    app = flask.Flask(__name__)

    @app.route("/test")
    def test_route():
        return "ok"

    @app.route("/static/<path>")
    def static_route(path):
        return "static"

    @app.route("/error")
    def error_route():
        raise ViewError()

    request_logger.bind_flask(app, get_user_id)
    return webtest.TestApp(app)


def pyramid_app(get_user_id=lambda args: "john"):
    pyramid = pytest.importorskip("pyramid")

    import pyramid.config

    config = pyramid.config.Configurator()
    config.add_route("test route", pattern="/test")
    config.add_route("error route", pattern="/error")
    config.add_route("static route", pattern="/static/{path}")
    config.add_view(lambda r: "ok", route_name="test route", renderer="string")
    config.add_view(lambda r: "static", route_name="static route", renderer="string")

    def error_view(request):
        raise ViewError()

    config.add_view(error_view, route_name="error route", renderer="string")

    request_logger.bind_pyramid(config, get_user_id)

    return webtest.TestApp(config.make_wsgi_app())


@pytest.fixture(params=[flask_app, pyramid_app])
def app(request, caplog):
    caplog.set_level(logging.INFO)
    return request.param()


@pytest.mark.parametrize("create_app", [flask_app, pyramid_app])
@pytest.mark.parametrize(
    "get_user_id", [lambda: 1 / 0, lambda: b"1", lambda: Exception()]
)
def test_exception_in_logger_doesnt_propagate(create_app, get_user_id, caplog):
    """Test that an error when fetching the user id or serializing it doesn't crash the app."""
    response = create_app(get_user_id).get("/test")
    assert response.status_code == 200
    assert not caplog.records


@pytest.mark.parametrize("create_app", [flask_app, pyramid_app])
def test_does_not_log_without_user(create_app, caplog):
    create_app(lambda: None).get("/test")
    assert not caplog.records


def test_does_not_log_when_hitting_static(app, caplog):
    app.get("/static/1")
    app.get("/static/2")
    assert not caplog.records


@pytest.mark.parametrize(
    "query,expected",
    [
        ("", {}),
        ("?name=j%C3%B3h%C3%B1&age=33", {"name": "jóhñ", "age": "33"}),
        ("?role=teacher&role=student", {"role": ["teacher", "student"]}),
    ],
)
def test_get_request(app, caplog, query, expected):
    app.get("/test{}".format(query))

    match = re.match(
        r"\[FullRequestInfo\] /test user=john args=(.*)", caplog.records[0].message
    )
    assert match and json.loads(match.group(1)) == expected


def test_when_error_request(app, caplog):
    try:
        app.get("/error", expect_errors=True)
    except Exception:
        pass
    assert caplog.records[0].message == "[FullRequestInfo] /error user=john args={}"
