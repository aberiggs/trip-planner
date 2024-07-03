"""Module providing integration test for signing in with google but signed up
with password"""

import json
import datetime
from datetime import timedelta
from unittest.mock import patch
from planner.http.error import GOOGLE_SIGN_IN_FAILED
from planner.util.password import hash_password
import pytest

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
    "password": hash_password("secure password"),
    "last_visited": utc_now.replace(tzinfo=None),
    "google_signup": False,
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
def patch_db_setup(client, rollback_session):
    """Function that provides fixture to patch auth.db_setup so that transactions
    are properly rolled back at the end of the test"""

    with patch(
        "auth.google_auth.db_setup",
        return_value=[client.trip_planner, rollback_session],
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


def test_google_signin_password_signup(
    patch_get_utc_now,
    patch_db_setup,
    patch_create_jwt_token,
    patch_google_verify_token,
    patch_get_secret,
    client,
    rollback_session,
):
    """Function that tests whether google_auth blocks users signed up with password"""

    from auth.google_auth import lambda_handler

    user_query = {"email": mock_id_info["email"]}

    # Expecting the user exists in the database before the user sign in
    client.trip_planner.users.insert_one(user_info, session=rollback_session)
    original_user = client.trip_planner.users.find_one(
        user_query, session=rollback_session
    )
    assert original_user == user_info

    event = {
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"id_token": "mock token", "client_type": "web"}),
    }

    lambda_response = lambda_handler(event, None)

    updated_user = client.trip_planner.users.find_one(
        user_query, session=rollback_session
    )

    # unsuccessful login should not update last_visited
    assert updated_user["last_visited"] == (utc_now).replace(tzinfo=None)
    assert lambda_response == GOOGLE_SIGN_IN_FAILED
