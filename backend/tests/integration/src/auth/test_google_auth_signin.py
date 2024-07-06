"""Module providing integration test for signing in with googe_auth"""

import json
from datetime import timedelta
from http import HTTPStatus
from unittest.mock import patch
import pytest
from planner.http.response import handle_response


@pytest.fixture
def patch_db_setup(user_repo):
    """Function that provides fixture to patch db_setup so that transactions
    are properly rolled back at the end of the test"""

    with patch(
        "auth.google_auth.db_setup",
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


def test_google_auth_signin(
    patch_get_utc_now,
    patch_db_setup,
    patch_create_jwt_token,
    patch_google_verify_token,
    patch_get_secret,
    mock_id_info,
    google_user,
    utc_now,
    user_repo,
):
    """Function that tests whether auth properly sign in non-existing users"""

    from planner.jwt.create_jwt_token import create_jwt_token
    from auth.google_auth import lambda_handler

    # Expecting the user exists in the database before the user sign in
    user_repo.insert_one(google_user)
    original_user = user_repo.find_one_by_email(mock_id_info["email"])
    assert original_user == google_user

    event = {
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"id_token": "mock token", "client_type": "web"}),
    }

    jwt_token = create_jwt_token({})
    lambda_response = lambda_handler(event, None)

    updated_user = user_repo.find_one_by_email(mock_id_info["email"])

    # check if the last_visited is updated
    assert updated_user["last_visited"] == (
        utc_now + timedelta(hours=1)
    ).replace(tzinfo=None)
    assert lambda_response == handle_response(
        {"code": HTTPStatus.OK.value, "body": {"jwt": jwt_token}}
    )
