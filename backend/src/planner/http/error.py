"""Module providing different error responses"""

from http import HTTPStatus
from planner.http.response import response_handler

INVALID_BODY = response_handler(
    400, {"message": "request body is an invalid JSON"}
)
INVALID_GOOGLE_ID_TOKEN = response_handler(
    HTTPStatus.UNAUTHORIZED, {"message": "invalid id_token"}
)
INVALID_CLIENT_TYPE = response_handler(
    HTTPStatus.UNAUTHORIZED, {"message": "invalid client_type"}
)
EMAIL_USED = response_handler(
    HTTPStatus.CONFLICT, {"message": "email already used"}
)
USER_NOT_EXIST = response_handler(
    HTTPStatus.UNAUTHORIZED,
    {"message": "user doesn't exist or password incorrect"},
)
GOOGLE_SIGN_IN_FAILED = response_handler(
    HTTPStatus.UNAUTHORIZED,
    {"message": "google sign in failed"},
)
PASSWORD_INCORRECT = response_handler(
    HTTPStatus.UNAUTHORIZED,
    {"message": "user doesn't exist or password incorrect"},
)
