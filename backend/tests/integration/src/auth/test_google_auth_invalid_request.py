"""Module providing integration test to test invalid request handling in google_auth"""

import json
from unittest.mock import patch
import datetime
import pytest
from planner.http.exception import (
    InvalidGoogleIdTokenException,
    InvalidClientTypeException,
    InvalidBodyException,
)
from planner.http.response import response_handler

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
def patch_google_verify_invalid_token():
    """Function that provides fixture to patch google.oauth2.id_token.verify_oauth2_token
    with invalid token"""

    with patch(
        "google.oauth2.id_token.verify_oauth2_token",
        side_effect=ValueError,
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
    """Function that provides fixture to patch db_setup so that transactions
    are properly rolled back at the end of the test"""

    with patch(
        "auth.google_auth.db_setup",
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


def test_auth_invalid_client_type(
    patch_get_utc_now,
    patch_db_setup,
    patch_create_jwt_token,
    patch_google_verify_token,
    patch_get_secret,
    user_repo,
):
    """Function that tests whether auth handles invalid client type"""

    from auth.google_auth import lambda_handler

    event = {
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {"id_token": "mock token", "client_type": "is this web?"}
        ),
    }

    assert not user_repo.find_one_by_email(mock_id_info["email"])

    lambda_response = lambda_handler(event, None)

    assert not user_repo.find_one_by_email(mock_id_info["email"])
    assert lambda_response == response_handler(
        InvalidClientTypeException().args[0]
    )


def test_auth_invalid_id_token(
    patch_get_utc_now,
    patch_db_setup,
    patch_create_jwt_token,
    patch_google_verify_invalid_token,
    patch_get_secret,
    user_repo,
):
    """Function that tests whether auth handles invalid id_token"""

    from auth.google_auth import lambda_handler

    event = {
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"id_token": "invalid token", "client_type": "web"}),
    }

    assert not user_repo.find_one_by_email(mock_id_info["email"])

    lambda_response = lambda_handler(event, None)

    assert not user_repo.find_one_by_email(mock_id_info["email"])
    assert lambda_response == response_handler(
        InvalidGoogleIdTokenException().args[0]
    )


def test_google_auth_invalid_request(
    patch_get_utc_now,
    patch_db_setup,
    patch_create_jwt_token,
    patch_google_verify_invalid_token,
    patch_get_secret,
    user_repo,
):
    """Function that tests whether auth handles invalid request body"""

    from auth.google_auth import lambda_handler

    event = {
        "headers": {"Content-Type": "application/json"},
        # this body is missing a double quote
        "body": '{"id_token: "mock token", "client_type": "web"}',
    }

    assert not user_repo.find_one_by_email(mock_id_info["email"])

    lambda_response = lambda_handler(event, None)

    assert not user_repo.find_one_by_email(mock_id_info["email"])
    assert lambda_response == response_handler(InvalidBodyException().args[0])
