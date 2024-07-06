"""Module providing common fixtures among auth integration tests"""

from unittest.mock import patch
import datetime
import pytest
from planner.util.password import hash_password

@pytest.fixture()
def utc_now():
    """Function providing fixture to use utc_now"""

    return datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)

@pytest.fixture()
def mock_id_info(utc_now):
    """Function providing fixture to use mock google id_info"""

    return {
        "given_name": "Bob",
        "family_name": "George",
        "picture": "picture.url",
        "email": "bob.george@email.com",
        "last_visited": utc_now,
        "plans": [],
    }

@pytest.fixture()
def google_user(mock_id_info, utc_now):
    """Function providing fixture to use mock user signed up with google"""

    return {
        "first_name": mock_id_info["given_name"],
        "last_name": mock_id_info["family_name"],
        "picture": mock_id_info["picture"],
        "email": mock_id_info["email"],
        "last_visited": utc_now.replace(tzinfo=None),
        "password": b"",
        "google_signup": True,
        "plans": [],
    }

@pytest.fixture()
def password_signin_info():
    """Function providing fixture to use mock signin_info for password sign in"""

    return {
        "first_name": "Steve",
        "last_name": "Bob",
        "picture": "",
        "email": "steve.bob@email.com",
        "password": "bob's secure password",
    }

@pytest.fixture()
def password_signup_info(password_signin_info):
    """Function providing fixture to use mock signin_info for password sign in"""

    return password_signin_info

@pytest.fixture()
def password_user(password_signin_info, utc_now):
    """Function providing fixture to use mock user signed up with password"""

    return {
        "first_name": password_signin_info["first_name"],
        "last_name": password_signin_info["last_name"],
        "picture": password_signin_info["picture"],
        "email": password_signin_info["email"],
        "last_visited": utc_now.replace(tzinfo=None),
        "password": hash_password(password_signin_info["password"]),
        "google_signup": False,
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
def patch_get_secret():
    """Function that provides fixture to patch planner.util.get_secret.get_secret"""

    with patch(
        "planner.util.get_secret.get_secret",
        return_value="mock_secret",
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
def patch_get_utc_now(utc_now):
    """Function that provides fixture to patch planner.util.get_utc_now.get_utc_now"""

    with patch(
        "planner.util.get_utc_now.get_utc_now",
        return_value=utc_now,
        autospec=True,
    ) as m:
        yield m
