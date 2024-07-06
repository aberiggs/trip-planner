"""Module providing integration test for signing up with password_signup"""

import json
import datetime
from http import HTTPStatus
from unittest.mock import patch
from planner.http.response import response_handler
from planner.util.password import check_password
import pytest

utc_now = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)

signup_info = {
    "first_name": "Steve",
    "last_name": "Bob",
    "email": "steve.bob@email.com",
    "password": "bob's secure password",
}

user_info = {
    "first_name": signup_info["first_name"],
    "last_name": signup_info["last_name"],
    "picture": "",
    "email": signup_info["email"],
    "last_visited": utc_now.replace(tzinfo=None),
    "google_signup": False,
    "plans": [],
}


@pytest.fixture
def patch_create_jwt_token():
    """Function that provides fixture to patch planner.jwt.create_jwt_token.create_jwt_token"""

    with patch(
        "planner.jwt.create_jwt_token.create_jwt_token",
        return_value="mock token",
        autospec=True,
    ) as m:
        yield m


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


@pytest.fixture
def patch_get_utc_now():
    """Function that provides fixture to patch planner.util.get_utc_now.get_utc_now"""

    with patch(
        "planner.util.get_utc_now.get_utc_now",
        return_value=utc_now,
        autospec=True,
    ) as m:
        yield m


def test_password_signup_valid_body(
    patch_get_utc_now,
    patch_db_setup,
    patch_create_jwt_token,
    user_repo,
):
    """Function that tests whether password_signin properly sign up non-existing users"""

    from planner.jwt.create_jwt_token import create_jwt_token
    from auth.password_signup import lambda_handler

    event = {
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "email": signup_info["email"],
                "password": signup_info["password"],
                "first_name": signup_info["first_name"],
                "last_name": signup_info["last_name"],
            }
        ),
    }

    jwt_token = create_jwt_token({})
    lambda_response = lambda_handler(event, None)

    new_user = user_repo.find_one_by_email(signup_info["email"])

    assert check_password(
        signup_info["password"].encode("utf-8"), new_user["password"]
    )

    new_user.pop("_id")
    new_user.pop("password")

    assert new_user == user_info
    assert lambda_response == response_handler(
        {"code": HTTPStatus.OK.value, "body": {"jwt": jwt_token}}
    )
