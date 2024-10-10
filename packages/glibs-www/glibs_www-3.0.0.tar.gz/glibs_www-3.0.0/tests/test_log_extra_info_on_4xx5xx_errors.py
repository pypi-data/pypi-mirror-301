import json
import logging
import pytest
import webtest

from glibs.www import log_extra_info_on_4xx5xx_errors

# App behavior
#
# Single endpoint /open-door
#
# Accepts GET (?door=X&passprahse=Y) or POST {"door": X, "passphrase": Y}
#
# Returns HTTP 400 if door is not geekie, using JSON
# Returns HTTP 403 if passphrase is not sempre em frente, not using JSON


def pyramid_app():
    pyramid = pytest.importorskip("pyramid")
    import pyramid.config
    import pyramid.httpexceptions

    def get(request):
        return get_or_post(request, **request.GET)

    def post(request):
        if request.headers["Content-Type"] != "application/json":
            request.response.status_int = 415
            return {"Content-Type": "expected application/json"}

        return get_or_post(request, **request.json_body)

    def get_or_post(request, door, passphrase, **extra):
        if door != "geekie":
            request.response.status_int = 404
            return {"door": "does not exist"}

        if passphrase != "sempreemfrente":
            raise pyramid.httpexceptions.HTTPForbidden()

        return {"open": True}

    config = pyramid.config.Configurator()
    config.add_route("open one door", pattern="/open-door")
    config.add_view(
        get, route_name="open one door", renderer="json", request_method="GET"
    )
    config.add_view(
        post, route_name="open one door", renderer="json", request_method="POST"
    )
    log_extra_info_on_4xx5xx_errors.bind_pyramid(config, log_maxsize=1000)
    return webtest.TestApp(config.make_wsgi_app())


def flask_app():
    flask = pytest.importorskip("flask")

    app = flask.Flask(__name__)

    def json_response(status, data):
        return flask.make_response(
            (json.dumps(data), status, {"Content-Type": "application/json"})
        )

    @app.route("/open-door", methods=["GET"])
    def get():
        return get_or_post(**flask.request.args.to_dict())

    @app.route("/open-door", methods=["POST"])
    def post():
        if flask.request.headers["Content-Type"] != "application/json":
            return json_response(415, {"Content-Type": "expected application/json"})

        return get_or_post(**flask.request.json)

    def get_or_post(door, passphrase, **extra):
        if door != "geekie":
            return json_response(404, {"door": "does not exist"})

        if passphrase != "sempreemfrente":
            flask.abort(403)

        return json_response(200, {"open": True})

    log_extra_info_on_4xx5xx_errors.bind_flask(app, log_maxsize=1000)
    return webtest.TestApp(app)


@pytest.fixture(params=[flask_app, pyramid_app])
def app(request, caplog):
    caplog.set_level(logging.INFO)
    return request.param()


def test_nothing_logged_when_status_code_200(app, caplog):
    app.get("/open-door", params={"door": "geekie", "passphrase": "sempreemfrente"})
    app.post(
        "/open-door",
        params=json.dumps({"door": "geekie", "passphrase": "sempreemfrente"}),
        headers={"Content-Type": "application/json"},
    )
    assert caplog.records == []


def test_response_logged_when_status_code_4xx_and_json_response(app, caplog):
    response = app.get(
        "/open-door",
        params={"door": "heaven", "passphrase": "abc123"},
        expect_errors=True,
    )
    assert response.status_code == 404
    assert '"door": "does not exist"' in caplog.text


def test_request_logged_when_status_code_4xx_and_json_request(app, caplog):
    response = app.post(
        "/open-door",
        params=json.dumps({"door": "heaven", "passphrase": "abc123"}),
        headers={"Content-Type": "application/json"},
        expect_errors=True,
    )
    assert response.status_code == 404
    assert '"door": "heaven"' in caplog.text


def test_no_crash_when_status_code_4xx_and_not_json_response(app):
    # Our forbidden handler intentionally "forgets" to return a JSON response
    response = app.get(
        "/open-door",
        params={"door": "geekie", "passphrase": "wrong"},
        expect_errors=True,
    )
    assert response.status_code == 403


def test_no_crash_when_status_code_4xx_and_not_json_request(app):
    response = app.post(
        "/open-door",
        params="not json",
        headers={"Content-Type": "text/plain"},
        expect_errors=True,
    )
    assert response.status_code == 415


def test_huge_requests_are_redacted(app, caplog):
    huge_request = json.dumps(
        dict(
            {"field_{}".format(i): "value_{}".format(i) for i in range(10000)},
            door="geekie",
            passphrase="wrong",
        )
    )
    response = app.post(
        "/open-door",
        params=huge_request,
        headers={"Content-Type": "application/json"},
        expect_errors=True,
    )
    assert response.status_code == 403  # KeyError("door")
    assert len(huge_request) > len(caplog.text)
