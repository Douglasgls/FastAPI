from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import UserList, UserPublic, UserSchema

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Olar Mundo!'}


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

    db_user = User(
        username=user.username,
        password=user.password,
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
    session: Session = Depends(get_session)
):
    users = session.scalars(
        select(User).limit(limit).offset(offset)
    )

    return {'users': users}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):

    exist_user = session.scalar(
        select(User).where(User.id == user_id)
    )

    if exist_user:
        exist_user.email = user.email
        exist_user.password = user.password
        exist_user.username = user.username

        session.add(exist_user)
        session.commit()
        session.refresh(exist_user)

        return exist_user

    else:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )


@app.delete('/users/{user_id}')
def delete_users(
    user_id: int, session: Session = Depends(get_session)
):
    exist_user = session.scalar(
        select(User).where(User.id == user_id)
    )

    if not exist_user:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )

    session.delete(exist_user)
    session.commit()

    return {'message': 'user deleted'}
