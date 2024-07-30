from sqlalchemy import select

from fast_zero.exception import UserBadRequest, UserDontHavePermission, UserNotFound
from fast_zero.models import User


class UserService:
    def __init__(self, session, current_user):
        self.current_user = current_user
        self.session = session

    def get_user(self, user_id):
        user = self.session.scalar(select(User).where(User.id == user_id))
        if user is None:
            raise UserNotFound()
        return user

    def create_user(self, username, email):
        user = User(username=username, email=email)
        self.session.add(user)
        self.session.commit()
        return user

    def update_user(self, user_id, user_data):
        if not user_data.username or not user_data.email:
            raise UserBadRequest()
        user = self.get_user(user_id)
        if not user:
            raise UserNotFound()

        if not self.has_permission(user_id):
            raise UserDontHavePermission()

        user.username = user_data.username
        user.email = user_data.email
        self.session.commit()
        return user

    def delete_user(self, user_id):
        user = self.get_user(user_id)
        if not self.has_permission(user_id):
            raise UserDontHavePermission()
        self.session.delete(user)
        self.session.commit()

    def has_permission(self, user_id):
        return user_id == self.current_user.id or self.current_user.is_admin
