from sqlalchemy import select

from fast_zero.models import User


def test_creat_user(session):

    user = User(
        username='Douglas',
        email='Doug@gmail.com',
        password='1234566'
    )

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'Doug@gmail.com')
    )

    assert result.username == 'Douglas'
