from datetime import datetime, timedelta
from http import HTTPStatus

import pytz
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User

pwd_context = PasswordHash.recommended()
oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = 'minha-chave-secreta'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_TIME = 30


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password_hash(plain_password: str, hash_password: str) -> bool:
    return pwd_context.verify(plain_password, hash_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=pytz.UTC) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_TIME
    )

    to_encode.update({'exp': expire})
    return encode(
        to_encode,
        SECRET_KEY,
        ALGORITHM
    )


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_schema),
    ):
    credencias_error = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Credencias inválidas',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = decode(
            token,
            SECRET_KEY,
            ALGORITHM
        )
        username = payload.get('sub')
        if not username:
            raise credencias_error
    except PyJWTError:
        raise credencias_error

    user_db = session.scalar(
        select(User).where(User.username == username)
    )

    if not user_db:
        raise credencias_error

    return user_db
