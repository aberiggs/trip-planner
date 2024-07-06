"""Module providing unit tests for jwt extractor"""

import time
import pytest
import jwt


def test_extract_jwt_normal(patch_get_secret) -> None:
    """Function that tests whether jwt validator catches token signed with a different key"""

    from planner.jwt.extractor import extract_jwt
    from planner.jwt.create_jwt_token import create_jwt_token

    payload = {
        "email": "chiweilien@gmail.com",
        "picture": "mypicture",
        "name": "Chi-Wei Lien",
    }

    token = create_jwt_token(payload)
    assert extract_jwt(token) == payload


def test_extract_jwt_signed_with_diff_secret(patch_get_secret) -> None:
    """Function that tests whether jwt extractor doesn't validate the token"""

    from planner.jwt.extractor import extract_jwt

    payload = {
        "email": "chiweilien@gmail.com",
        "picture": "mypicture",
        "name": "Chi-Wei Lien",
    }

    token = jwt.encode(
        payload,
        "fake_secret",
        algorithm="HS256",
        headers={"exp": int(time.time()) + 864000},
    )

    try:
        extracted_payload = extract_jwt(token)
    except Exception as e:
        pytest.fail(f"handle_response raised an exception: {e}")

    assert extracted_payload == payload
