class UserServiceError(Exception):
    ...


class UserDoesNotExistError(UserServiceError):
    ...


class UserAlreadyExistError(UserServiceError):
    ...
