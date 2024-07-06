"""Module providing integration test for signing in with google but signed up
with password"""

import json
from unittest.mock import patch
import pytest
from planner.http.exception import GoogleSignInFailedException
from planner.http.response import response_handler

# @pytest.fixture()
# def google_user(mock_id_info, utc_now):
#     """Function providing fixture to use mock google id_info"""

#     return {
#         "first_name": mock_id_info["given_name"],
#         "last_name": mock_id_info["family_name"],
#         "picture": mock_id_info["picture"],
#         "email": mock_id_info["email"],
#         "last_visited": utc_now.replace(tzinfo=None),
#         "password": b"",
#         "google_signup": False,
#         "plans": [],
#     }


@pytest.fixture()
def mock_id_info(utc_now, password_user):
    """Function providing fixture to use mock google id_info"""

    return {
        "given_name": password_user["first_name"],
        "family_name": password_user["last_name"],
        "picture": password_user["picture"],
        "email": password_user["email"],
        "last_visited": utc_now,
        "plans": [],
    }

@pytest.fixture
def patch_google_verify_token(mock_id_info):
    """Function that provides fixture to patch google.oauth2.id_token.verify_oauth2_token"""

    with patch(
        "google.oauth2.id_token.verify_oauth2_token",
        return_value=mock_id_info,
        autospec=True,
    ) as m:
        yield m

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

def test_google_signin_password_signup(
    patch_get_utc_now,
    patch_db_setup,
    patch_create_jwt_token,
    patch_google_verify_token,
    patch_get_secret,
    mock_id_info,
    password_user,
    utc_now,
    user_repo,
):
    """Function that tests whether google_auth blocks users signed up with password"""

    from auth.google_auth import lambda_handler

    # Expecting the user exists in the database before the user sign in
    user_repo.insert_one(password_user)
    original_user = user_repo.find_one_by_email(password_user["email"])
    assert original_user == password_user

    event = {
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"id_token": "mock token", "client_type": "web"}),
    }

    lambda_response = lambda_handler(event, None)

    updated_user = user_repo.find_one_by_email(password_user["email"])

    # unsuccessful login should not update last_visited
    assert updated_user["last_visited"] == (utc_now).replace(tzinfo=None)
    assert lambda_response == response_handler(
        GoogleSignInFailedException().args[0]
    )
