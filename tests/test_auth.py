from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, create_fake_user):
    response = client.post(
        'auth/token',
        data={
            'username': create_fake_user.email,
            'password': create_fake_user.clean_password
        }
    )

    assert response.status_code == HTTPStatus.OK


def test_token_expired_after_time(client, create_fake_user):
    """ manipulando o tempo com o freeze_time """
    with freeze_time('2025-07-14 12:00:00'):
        response = client.post(
        'auth/token',
        data={
            'username': create_fake_user.email,
            'password': create_fake_user.clean_password
        }
    )
    assert response.status_code == HTTPStatus.OK
    expire_token = response.json()['access_token']
    with freeze_time('2025-07-14 12:32:00'):
        response = client.put(
        f'/users/{create_fake_user.id}',
        headers={'Authorization': f'Bearer {expire_token}'},
        json={
            'username': 'Testeatualizado',
            'email': 'Testeatualizado@gmail.com',
            'password': '123456'
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_refresh_token(client, token):
    response = client.post(
        'auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'}
    )

    response.status_code == HTTPStatus.OK
