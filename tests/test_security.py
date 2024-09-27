from http import HTTPStatus

from jwt import decode

from fast_zero.security import create_access_token
from fast_zero.settings import Settings

settings = Settings()


def test_access_token():
    data = {'sub': 'test@Test.com'}
    token = create_access_token(data)

    result = decode(
        jwt=token, key=settings.SECRET_KEY,
        algorithms=settings.ALGORITHM
    )

    assert result['sub'] == 'test@Test.com'
    assert result['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Credencias inválidas'}
