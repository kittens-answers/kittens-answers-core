class ServiceError(Exception):
    ...


class UserDoesNotExistError(ServiceError):
    ...


class UserAlreadyExistError(ServiceError):
    ...


class QuestionAlreadyExistError(ServiceError):
    ...


class QuestionDoesNotExistError(ServiceError):
    ...
