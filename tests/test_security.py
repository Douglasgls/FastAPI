from http import HTTPStatus

from jwt import decode

from fast_zero.security import ALGORITHM, SECRET_KEY, create_access_token


def test_access_token():
    data = {'sub': 'test@Test.com'}
    token = create_access_token(data)

    result = decode(jwt=token, key=SECRET_KEY, algorithms=ALGORITHM,)

    assert result['sub'] == 'test@Test.com'
    assert result['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
