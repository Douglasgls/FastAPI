from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Token, UserList, UserPublic, UserSchema
from fast_zero.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password_hash,
)

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Olar Mundo!'}


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
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


@app.post('/users',
        status_code=status.HTTP_201_CREATED,
        response_model=UserPublic
    )
def create_user(user: UserSchema, session: Session = Depends(get_session)):
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


@app.get('/users', response_model=UserList)
def get_users(
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    users = session.scalars(
        select(User).limit(limit).offset(offset)
    )

    return {'users': users}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=400,
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


@app.delete('/users/{user_id}')
def delete_users(
    user_id: int, session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=400,
            detail='Esse usuário não tem permissão para alterar outro'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'user deleted'}
