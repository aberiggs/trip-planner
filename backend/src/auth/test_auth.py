"""Module providing the handler for the test auth endpoint"""

from http import HTTPStatus
from planner.jwt.validator import validate_jwt
from planner.http.validator import validate_header
from planner.http.response import handle_response


def lambda_handler(event, context):
    """Lambda handler that checks whether the current user is signed in"""

    validate_header_response = validate_header(event, ["Authorization"])

    if validate_header_response is not None:
        return validate_header_response

    jwt_token = event["headers"]["Authorization"].split(" ")[1].encode("utf-8")

    if validate_jwt(jwt_token):
        return handle_response(
            {
                "code": HTTPStatus.OK.value,
                "body": {"message": "you are logged in"},
            }
        )

    return handle_response(
        {
            "code": HTTPStatus.UNAUTHORIZED.value,
            "body": {"message": "you are not logged in"},
        }
    )
