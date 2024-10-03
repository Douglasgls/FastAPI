import factory
import factory.fuzzy
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import Todos, TodoState, User, table_registry
from fast_zero.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:  # Quem sera construido ?
        model = User

    username = factory.sequence(lambda n=1: f"teste{n}")
    email = factory.lazy_attribute(lambda obj: f'{obj.username}@test.com')
    password = factory.lazy_attribute(lambda obj: f'{obj.username}+senha')


class TodoFactory(factory.Factory):
    class Meta:
        model = Todos

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


@pytest.fixture
def client(session):

    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:

        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def create_fake_user(session):
    pwd = '12345'
    user = UserFactory(
        password=get_password_hash(pwd)
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd  # Monkey patch
    return user


@pytest.fixture
def create_fake_other_user(session):
    pwd = '12345'
    user = UserFactory(
        password=get_password_hash(pwd)
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def token(client, create_fake_user):
    response = client.post(
        'auth/token',
        data={
            'username': create_fake_user.email,
            'password': create_fake_user.clean_password
        }
    )
    response_json = response.json()
    return response_json['access_token']
