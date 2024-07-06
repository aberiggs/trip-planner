"""Module providing integration test for signing in with password_signup"""

import json
from datetime import timedelta
from http import HTTPStatus
from unittest.mock import patch
from planner.http.response import handle_response
import pytest


@pytest.fixture
def patch_db_setup(user_repo):
    """Function that provides fixture to patch db_setup so that transactions
    are properly rolled back at the end of the test"""

    with patch(
        "auth.password_signin.db_setup",
        return_value=user_repo,
        autospec=True,
    ) as m:
        yield m


@pytest.fixture
def patch_get_utc_now(utc_now):
    """Function that provides fixture to patch planner.util.get_utc_now.get_utc_now"""

    with patch(
        "planner.util.get_utc_now.get_utc_now",
        return_value=utc_now + timedelta(hours=1),
        autospec=True,
    ) as m:
        yield m


def test_password_signin(
    patch_get_utc_now,
    patch_db_setup,
    patch_create_jwt_token,
    password_user,
    password_signin_info,
    utc_now,
    user_repo,
):
    """Function that tests whether password_signin properly sign in existing users"""

    from planner.jwt.create_jwt_token import create_jwt_token
    from auth.password_signin import lambda_handler

    # Expecting the user exists in the database before the user sign in
    user_repo.insert_one(password_user)
    original_user = user_repo.find_one_by_email(password_signin_info["email"])
    assert original_user == password_user

    event = {
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "email": password_signin_info["email"],
                "password": password_signin_info["password"],
            }
        ),
    }

    jwt_token = create_jwt_token({})
    lambda_response = lambda_handler(event, None)

    updated_user = user_repo.find_one_by_email(password_signin_info["email"])

    # check if the last_visited is updated
    assert updated_user["last_visited"] == (
        utc_now + timedelta(hours=1)
    ).replace(tzinfo=None)
    assert lambda_response == handle_response(
        {"code": HTTPStatus.OK.value, "body": {"jwt": jwt_token}}
    )
