"""Module that provides function that get JWT token from header"""

from planner.http.validator import header_validator


def get_jwt_token(event):
    """Function that checks whether the user is signed in"""
    header_validator(event, ["Authorization"])

    return event["headers"]["Authorization"].split(" ")[1].encode("utf-8")
