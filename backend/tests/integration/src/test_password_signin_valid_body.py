"""Module providing integration test for signing in with password_signup"""

import json
import datetime
from datetime import timedelta
from http import HTTPStatus
from unittest.mock import patch
from planner.http.response import response_handler
from planner.util.password import hash_password
import pytest

utc_now = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)

signin_info = {
    "first_name": "Steve",
    "last_name": "Bob",
    "picture": "steve.bob.png",
    "email": "steve.bob@email.com",
    "password": "bob's secure password",
}

user_info = {
    "first_name": signin_info["first_name"],
    "last_name": signin_info["last_name"],
    "picture": signin_info["picture"],
    "email": signin_info["email"],
    "password": hash_password(signin_info["password"]),
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
def patch_db_setup(client, rollback_session):
    """Function that provides fixture to patch auth.db_setup so that transactions
    are properly rolled back at the end of the test"""

    with patch(
        "auth.password_signin.db_setup",
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


def test_password_signin_valid_body(
    patch_get_utc_now,
    patch_db_setup,
    patch_create_jwt_token,
    client,
    rollback_session,
):
    """Function that tests whether password_signin properly sign in existing users"""

    from planner.jwt.create_jwt_token import create_jwt_token
    from auth.password_signin import lambda_handler

    user_query = {"email": signin_info["email"]}

    # Expecting the user exists in the database before the user sign in
    client.trip_planner.users.insert_one(user_info, session=rollback_session)
    original_user = client.trip_planner.users.find_one(
        user_query, session=rollback_session
    )
    assert original_user == user_info

    event = {
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "email": signin_info["email"],
                "password": signin_info["password"],
            }
        ),
    }

    jwt_token = create_jwt_token({})
    lambda_response = lambda_handler(event, None)

    updated_user = client.trip_planner.users.find_one(
        user_query, session=rollback_session
    )

    # check if the last_visited is updated
    assert updated_user["last_visited"] == (
        utc_now + timedelta(hours=1)
    ).replace(tzinfo=None)
    assert lambda_response == response_handler(
        HTTPStatus.OK, {"jwt": jwt_token}
    )
