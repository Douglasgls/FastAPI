from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_read_root_must_return_ok_and_hello_word():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
