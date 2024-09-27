from http import HTTPStatus

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Todos, User
from fast_zero.schemas import TodoPublic, TodoSchema, TodoUpdate
from fast_zero.security import get_current_user

router = APIRouter(
    prefix='/todos',
    tags=['todos']
)


@router.post('/', response_model=TodoPublic)
def create_todo(
    todo: TodoSchema,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    ):

    db_todo = Todos(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/')
def list_todos(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    title: str = Query(None),
    description: str = Query(None),
    state: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Todos).where(User.id == current_user.id)

    if title:
        query = query.filter(
            Todos.title.contains(title)
        )

    if description:
        query = query.filter(
            Todos.description.contains(description)
        )

    if state:
        query = query.filter(
            Todos.state == state
        )

    todos = session.scalars(
        query.offset(offset).limit(limit)
    ).all()

    return {
        'todos': todos
    }


@router.delete('/{id_todos}')
def delete_todo(
    id_todos: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):

    print(id_todos)
    exist_query = session.scalar(
        select(Todos).where(
        Todos.id == id_todos, Todos.user_id == current_user.id
    ))

    if not exist_query:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Task not found.'
        )

    session.delete(
        exist_query
    )
    session.commit()
    return {'message': 'Task has been deleted successfully.'}


@router.patch('/{id_todos}')
def update_todo(
    id_todos: int,
    todo: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):

    db_todo = session.scalar(
        select(Todos).where(
            Todos.id == id_todos, Todos.user_id == current_user.id
        )
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Task not found.'
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
