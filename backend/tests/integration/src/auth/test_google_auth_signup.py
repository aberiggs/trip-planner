"""Module providing integration test for signing up with googe_auth"""

import json
from http import HTTPStatus
from unittest.mock import patch
from planner.http.response import handle_response
import pytest

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


def test_google_auth_signup(
    patch_get_utc_now,
    patch_db_setup,
    patch_create_jwt_token,
    patch_google_verify_token,
    patch_get_secret,
    mock_id_info,
    google_user,
    user_repo,
):
    """Function that tests whether auth properly sign up non-existing users"""

    from planner.jwt.create_jwt_token import create_jwt_token
    from auth.google_auth import lambda_handler

    event = {
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"id_token": "mock token", "client_type": "web"}),
    }

    assert not user_repo.find_one_by_email(mock_id_info["email"])

    jwt_token = create_jwt_token({})
    lambda_response = lambda_handler(event, None)

    new_user = user_repo.find_one_by_email(mock_id_info["email"])
    new_user.pop("_id")

    assert new_user == google_user
    assert lambda_response == handle_response(
        {"code": HTTPStatus.OK.value, "body": {"jwt": jwt_token}}
    )
