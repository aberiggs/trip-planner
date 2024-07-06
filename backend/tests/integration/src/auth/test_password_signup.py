"""Module providing integration test for signing up with password_signup"""

import json
from http import HTTPStatus
from unittest.mock import patch
from planner.http.response import handle_response
from planner.util.password import check_password
import pytest

@pytest.fixture
def patch_db_setup(user_repo):
    """Function that provides fixture to patch db_setup so that transactions
    are properly rolled back at the end of the test"""

    with patch(
        "auth.password_signup.db_setup",
        return_value=user_repo,
        autospec=True,
    ) as m:
        yield m

def test_password_signup(
    patch_get_utc_now,
    patch_db_setup,
    patch_create_jwt_token,
    password_signup_info,
    password_user,
    user_repo,
):
    """Function that tests whether password_signin properly sign up non-existing users"""

    from planner.jwt.create_jwt_token import create_jwt_token
    from auth.password_signup import lambda_handler

    event = {
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "email": password_signup_info["email"],
                "password": password_signup_info["password"],
                "first_name": password_signup_info["first_name"],
                "last_name": password_signup_info["last_name"],
            }
        ),
    }

    jwt_token = create_jwt_token({})
    lambda_response = lambda_handler(event, None)

    new_user = user_repo.find_one_by_email(password_signup_info["email"])

    assert check_password(
        password_signup_info["password"].encode("utf-8"), new_user["password"]
    )

    new_user.pop("_id")
    new_user.pop("password")
    password_user.pop("password")

    assert new_user == password_user
    assert lambda_response == handle_response(
        {"code": HTTPStatus.OK.value, "body": {"jwt": jwt_token}}
    )
