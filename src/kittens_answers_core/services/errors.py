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


class AnswerAlreadyExistError(ServiceError):
    ...


class AnswerDoesNotExistError(ServiceError):
    ...
