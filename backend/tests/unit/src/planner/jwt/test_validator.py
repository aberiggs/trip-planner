"""Module providing unit tests for jwt validator"""

import time
import jwt

def test_validate_jwt_signed_with_diff_secret(patch_get_secret) -> None:
    """Function that tests whether jwt validator catches token signed with a different key"""

    from planner.jwt.validator import validate_jwt

    payload = {
        "email": "chiweilien@gmail.com",
        "picture": "mypicture",
        "name": "Chi-Wei Lien",
    }

    token = jwt.encode(
        payload,
        "fake_secret",
        algorithm="HS256",
        headers={"exp": int(time.time()) + 864000},  # ten days
    )

    assert validate_jwt(token) is False

def test_validate_jwt_signed_with_same_secret(patch_get_secret) -> None:
    """Function that tests whether jwt validator returns true when token is
    signed with the same key"""

    from planner.jwt.validator import validate_jwt
    from planner.jwt.create_jwt_token import create_jwt_token

    payload = {
        "email": "chiweilien@gmail.com",
        "picture": "mypicture",
        "name": "Chi-Wei Lien",
    }

    token = create_jwt_token(payload, int(time.time()) + 864000)  # ten days

    assert validate_jwt(token) is True

def test_validate_jwt_expired_jwt(patch_get_secret) -> None:
    """Function that tests whether jwt validator catches expired token"""

    from planner.jwt.validator import validate_jwt
    from planner.jwt.create_jwt_token import create_jwt_token

    payload = {
        "email": "chiweilien@gmail.com",
        "picture": "mypicture",
        "name": "Chi-Wei Lien",
    }

    token = create_jwt_token(payload, int(time.time()) - 10)

    assert validate_jwt(token) is False

def test_validate_jwt_no_exp(patch_get_secret) -> None:
    """Function that tests whether jwt validator returns true when token
    hasn't expired"""

    from planner.jwt.validator import validate_jwt

    payload = {
        "email": "chiweilien@gmail.com",
        "picture": "mypicture",
        "name": "Chi-Wei Lien",
    }

    token = jwt.encode(
        payload,
        "mock_secret",
        algorithm="HS256",
    )

    assert validate_jwt(token) is False
