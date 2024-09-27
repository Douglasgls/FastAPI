from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Token
from fast_zero.security import (
    create_access_token,
    get_current_user,
    verify_password_hash,
)

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

T_Session = Annotated[Session, Depends(get_session)]  # Motivo do T_ é  devido a conveção python veja sobre: https://peps.python.org/pep-0008/#type-variable-names


@router.post('/token', response_model=Token)
def login_for_access_token(
    session: T_Session,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user_db = session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user_db or not verify_password_hash(
        form_data.password,
        user_db.password
        ):
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Incorrect email or password '
            )

    token = create_access_token(data={'sub': user_db.username})

    return {
        'access_token': token,
        'token_type': 'Bearer'
    }


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(
    user: User = Depends(get_current_user),
):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
