"""Module providing integration test for signing in with password but signed up
with google"""

import json
import datetime
from datetime import timedelta
from unittest.mock import patch
import pytest
from planner.http.response import response_handler
from planner.http.exception import UserNotExistException

utc_now = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)

mock_id_info = {
    "given_name": "Bob",
    "family_name": "George",
    "picture": "picture.url",
    "email": "bob.george@email.com",
    "last_visited": utc_now,
    "plans": [],
}

user_info = {
    "first_name": mock_id_info["given_name"],
    "last_name": mock_id_info["family_name"],
    "picture": mock_id_info["picture"],
    "email": mock_id_info["email"],
    "last_visited": utc_now.replace(tzinfo=None),
    "password": b"",
    "google_signup": True,
    "plans": [],
}


@pytest.fixture
def patch_get_secret():
    """Function that provides fixture to patch planner.util.get_secret.get_secret"""

    with patch(
        "planner.util.get_secret.get_secret",
        return_value="mock_secret",
        autospec=True,
    ) as m:
        yield m


@pytest.fixture
def patch_google_verify_token():
    """Function that provides fixture to patch google.oauth2.id_token.verify_oauth2_token"""

    with patch(
        "google.oauth2.id_token.verify_oauth2_token",
        return_value=mock_id_info,
        autospec=True,
    ) as m:
        yield m


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
    """Function that provides fixture to patch auth.db_setup so that transactions
    are properly rolled back at the end of the test"""

    with patch(
        "auth.password_signin.db_setup",
        return_value=user_repo,
        autospec=True,
    ) as m:
        yield m


@pytest.fixture
def patch_get_utc_now():
    """Function that provides fixture to patch planner.util.get_utc_now.get_utc_now"""

    with patch(
        "planner.util.get_utc_now.get_utc_now",
        return_value=utc_now + timedelta(hours=1),
        autospec=True,
    ) as m:
        yield m


def test_password_signin_google_signup(
    patch_get_utc_now,
    patch_db_setup,
    patch_create_jwt_token,
    patch_google_verify_token,
    patch_get_secret,
    user_repo,
):
    """Function that tests whether password_signin blocks users signed up with google"""

    from auth.password_signin import lambda_handler

    # Expecting the user exists in the database before the user sign in
    user_repo.insert_one(user_info)
    original_user = user_repo.find_one_by_email(mock_id_info["email"])
    assert original_user == user_info

    event = {
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "email": user_info["email"],
                "password": "",
            }
        ),
    }

    lambda_response = lambda_handler(event, None)
    updated_user = user_repo.find_one_by_email(mock_id_info["email"])

    # unsuccessful login should not update last_visited
    assert updated_user["last_visited"] == (utc_now).replace(tzinfo=None)
    assert lambda_response == response_handler(UserNotExistException().args[0])
