"""Module providing the handler for the test auth endpoint"""

from planner.jwt.validator import jwt_validator
from planner.http.validator import header_validator
from planner.http.response import response_handler


def lambda_handler(event, context):
    """Lambda handler that checks whether the current user is signed in"""

    header_validator_response = header_validator(event, ["Authorization"])

    if header_validator_response is not None:
        return header_validator_response

    jwt_token = event["headers"]["Authorization"].split(" ")[1].encode("utf-8")

    if jwt_validator(jwt_token):
        return response_handler(200, {"message": "you are logged in"})

    return response_handler(401, {"message": "you are not logged in"})
