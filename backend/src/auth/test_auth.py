"""Module providing the handler for the test auth endpoint"""

from http import HTTPStatus
from planner.http.response import handle_response
from planner.http.exception import HttpException
from planner.middleware.check_user_signin import check_user_signin

def lambda_handler(event, context):
    """Lambda handler that checks whether the current user is signed in"""

    try:
        check_user_signin(event)

        return handle_response(
            {
                "code": HTTPStatus.OK.value,
                "body": {"message": "you are authorized"},
            }
        )

    except HttpException as e:
        return handle_response(e.args[0])
