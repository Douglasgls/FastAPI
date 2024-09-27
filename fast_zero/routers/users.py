from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import UserList, UserPublic, UserSchema
from fast_zero.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(
    prefix='/users',
    tags=['users']
)

T_Session = Annotated[Session, Depends(get_session)]
T_Current_user = Annotated[User, Depends(get_current_user)]


@router.post('/',
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublic
)
def create_user(
    session: T_Session,
    user: UserSchema,
):
    exists_user = session.scalar(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    )
    if exists_user:
        if exists_user.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already exists'
            )
        if exists_user.username == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username already exists'
            )

    hash_password = get_password_hash(user.password)

    db_user = User(
        username=user.username,
        password=hash_password,
        email=user.email
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList)
def get_users(
    current_user: T_Current_user,
    session: T_Session,
    limit: int = 10,
    offset: int = 0,
):
    users = session.scalars(
        select(User).limit(limit).offset(offset)
    )

    return {'users': users}


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: T_Session,
    current_user: T_Current_user,
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Esse usuário não tem permissão para alterar outro'
        )

    hash_password = get_password_hash(user.password)
    current_user.email = user.email
    current_user.password = hash_password
    current_user.username = user.username

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}')
def delete_users(
    user_id: int, session: T_Session,
    current_user: T_Current_user,
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Esse usuário não tem permissão para alterar outro'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'user deleted'}
