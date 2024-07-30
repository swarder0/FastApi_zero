from http import HTTPStatus


class UserNotFound(Exception):
    def __init__(self):
        self.message = "User not found"
        self.status_code = HTTPStatus.NOT_FOUND
        super().__init__(self.message)


class UserDontHavePermission(Exception):
    def __init__(self):
        self.message = "Not enough permissions"
        self.status_code = HTTPStatus.FORBIDDEN
        super().__init__(self.message)


class UserBadRequest(Exception):
    def __init__(self):
        self.message = "Bad request"
        self.status_code = HTTPStatus.BAD_REQUEST
        super().__init__(self.message)
