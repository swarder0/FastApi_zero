from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username="Teste do banco",
        email="mail.test@email.com",
        password="supersenhasegura",
    )
    session.add(user)
    session.commit()
    session.scalar(select(User).where(User.email == "mail.test@email.com"))

    assert user.username == "Teste do banco"
