"""Module providing different error responses"""

from planner.http.response import response_handler

INVALID_BODY = response_handler(
    400, {"message": "request body is an invalid JSON"}
)
INVALID_GOOGLE_ID_TOKEN = response_handler(401, {"message": "invalid id_token"})
INVALID_CLIENT_TYPE = response_handler(401, {"message": "invalid client_type"})
EMAIL_USED = response_handler(409, {"message": "email already used"})
USER_NOT_EXIST = response_handler(
    401, {"message": "user doesn't exist or password incorrect"}
)
PASSWORD_INCORRECT = response_handler(
    401, {"message": "user doesn't exist or password incorrect"}
)
