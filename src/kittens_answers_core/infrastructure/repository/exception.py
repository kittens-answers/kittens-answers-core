class RepositoryException(Exception):
    ...


class AnswerAlreadyExistException(RepositoryException):
    ...


class AnswerNotFoundException(RepositoryException):
    ...


class MarkAlreadyExistException(RepositoryException):
    ...


class NotingToUpdateException(RepositoryException):
    ...


class MarkNotExistException(RepositoryException):
    ...


class QuestionNotFoundException(RepositoryException):
    ...


class QuestionAlreadyExistException(RepositoryException):
    ...


class UserNotFoundException(RepositoryException):
    ...


class UserAlreadyExistException(RepositoryException):
    ...
