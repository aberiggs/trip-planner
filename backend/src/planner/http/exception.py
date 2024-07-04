"""Module providing different http exceptions"""

from http import HTTPStatus


class HttpException(Exception):
    """Class that provides base exception for http errors"""


class InvalidBodyException(HttpException):
    """Class that provides exception to handle cases where body passed in is invalid"""

    def __init__(self):
        super().__init__(
            {
                "code": HTTPStatus.BAD_REQUEST,
                "body": {"message": "request body is an invalid JSON"},
            }
        )


class InvalidGoogleIdTokenException(HttpException):
    """Class that provides exception to handle cases where id token from Google is invalid"""

    def __init__(self):
        super().__init__(
            {
                "code": HTTPStatus.UNAUTHORIZED,
                "body": {"message": "invalid id_token"},
            }
        )


class InvalidClientTypeException(HttpException):
    """Class that provides exception to handle cases where client type for google auth is invalid"""

    def __init__(self):
        super().__init__(
            {
                "code": HTTPStatus.UNAUTHORIZED,
                "body": {"message": "invalid client_type"},
            }
        )


class EmailUsedException(HttpException):
    """Class that provides exception to handle cases where email is already used
    when signing up with password"""

    def __init__(self):
        super().__init__(
            {
                "code": HTTPStatus.CONFLICT,
                "body": {"message": "email already used"},
            }
        )


class UserNotExistException(HttpException):
    """Class that provides exception to handle cases where user doesn't exist when
    signing in with password"""

    def __init__(self):
        super().__init__(
            {
                "code": HTTPStatus.UNAUTHORIZED,
                "body": {"message": "user doesn't exist or password incorrect"},
            }
        )


class GoogleSignInFailedException(HttpException):
    """Class that provides exception to handle cases where user doesn't sign up
    with Google but try to login with Google"""

    def __init__(self):
        super().__init__(
            {
                "code": HTTPStatus.UNAUTHORIZED,
                "body": {"message": "user doesn't exist or password incorrect"},
            }
        )


class PasswordIncorrectException(HttpException):
    """Class that provides exception to handle cases where password is incorrect
    when signing in with password"""

    def __init__(self):
        super().__init__(
            {
                "code": HTTPStatus.UNAUTHORIZED,
                "body": {"message": "user doesn't exist or password incorrect"},
            }
        )


class ResourceNotFoundException(HttpException):
    """Class that provides generic exception to handle cases where resource cannot
    be found"""

    def __init__(self):
        super().__init__(
            {
                "code": HTTPStatus.NOT_FOUND,
                "body": {"message": "resource cannot be found"},
            }
        )


class InvalidPlanDateException(HttpException):
    """Class that provides exception to handle cases where plan's date is in incorrect
    format"""

    def __init__(self):
        super().__init__(
            {
                "code": HTTPStatus.BAD_REQUEST,
                "body": {
                    "message": "plan date should follow the format: %m/%d/%y"
                },
            }
        )
