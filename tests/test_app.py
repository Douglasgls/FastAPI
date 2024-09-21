from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root_must_return_ok_and_hello_word(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK


def test_creat_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Douglas',
            'email': 'DouglasPaz@gmail.com',
            'password': '123456'
        }

    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'Douglas',
        'email': 'DouglasPaz@gmail.com',
        }


def test_read_users(client):
    response = client.get(
        '/users',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_with_user(client, create_fake_user):
    user_schema = UserPublic.model_validate(create_fake_user).model_dump()
    response = client.get(
        '/users/',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, create_fake_user):
    response = client.put(
        '/users/1',
        json={
            'username': 'Testeatualizado',
            'email': 'Testeatualizado@gmail.com',
            'password': '123456'
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Testeatualizado',
        'email': 'Testeatualizado@gmail.com',
        }


def test_delete_user(client, create_fake_user):
    response = client.delete(
        '/users/1'
    )
    assert response.status_code == HTTPStatus.OK
