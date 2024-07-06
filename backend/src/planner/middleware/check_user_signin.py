"""Module providing the middleware that checks whether the user is signed in"""

from planner.jwt.validator import validate_jwt
from planner.jwt.get_jwt_token import get_jwt_token
from planner.http.exception import UnauthroizedException


def check_user_signin(event):
    """Function that checks whether the user is signed in"""

    if not validate_jwt(get_jwt_token(event)):
        raise UnauthroizedException
