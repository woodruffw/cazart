import pytest
from schema import Schema

from cazart import bad_json, validation_error


def test_validates(cazart):
    result = None

    @cazart.route("/", schema=Schema({"name": str}))
    def root(res):
        nonlocal result
        result = res
        return ("ok", 200)

    with cazart.flask.test_client() as client:
        resp = client.get("/", json={"name": "foo"})
        assert resp.data == b"ok"
        assert resp.status_code == 200
        assert result == {"name": "foo"}


def test_does_not_validate(cazart):
    @cazart.route("/", schema=Schema({"name": str}))
    def root(res):
        return ("ok", 200)

    with cazart.flask.test_client() as client:
        resp = client.get("/", json={"name": 1234})
        assert resp.data == b"Key 'name' error:\n1234 should be instance of 'str'"
        assert resp.status_code == 400
        assert bad_json == {"name": 1234}
        assert validation_error == "Key 'name' error:\n1234 should be instance of 'str'"


def test_missing_json(cazart):
    @cazart.route("/", schema=Schema({"name": str}))
    def root(res):
        return ("ok", 200)

    with cazart.flask.test_client() as client:
        resp = client.get("/")
        assert resp.data == b"missing or malformed JSON"
        assert resp.status_code == 400


def test_malformed_json(cazart):
    @cazart.route("/", schema=Schema({"name": str}))
    def root(res):
        return ("ok", 200)

    with cazart.flask.test_client() as client:
        resp = client.get("/", data="{'bad json'}")
        assert resp.data == b"missing or malformed JSON"
        assert resp.status_code == 400


@pytest.mark.parametrize(
    ("method", "json", "exp_data", "status_code", "exp_result"),
    [
        ("GET", {"id": 1234}, b"ok", 200, {"id": 1234}),
        ("GET", {"name": "foo"}, b"Missing key: 'id'", 400, None),
        ("POST", {"name": "foo"}, b"ok", 200, {"name": "foo"}),
        ("POST", {"id": 1234}, b"Missing key: 'name'", 400, None),
    ],
)
def test_routes_methods(cazart, method, json, exp_data, status_code, exp_result):
    result = None

    @cazart.route("/", schema={"GET": Schema({"id": int}), "POST": Schema({"name": str})})
    def root(res):
        nonlocal result
        result = res
        return ("ok", 200)

    with cazart.flask.test_client() as client:
        resp = client.open(method=method, json=json)
        assert resp.data == exp_data
        assert resp.status_code == status_code

        if exp_result is not None:
            assert result == exp_result
