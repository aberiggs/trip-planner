"""Module providing unit tests for jwt extractor"""

import time
from unittest import TestCase
from unittest.mock import patch
import pytest
import jwt


class TestExtractor(TestCase):
    """Class containing all unit tests for jwt extractor"""

    def setUp(self) -> None:
        """Setup function that patches the result of
        planner.util.get_secret.get_secret to mock_secret"""

        self.patcher = patch(
            "planner.util.get_secret.get_secret", return_value="mock_secret"
        )
        self.patcher.start()

    def test_extract_jwt_normal(self) -> None:
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

    def test_extract_jwt_signed_with_diff_secret(self) -> None:
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

    def tearDown(self) -> None:
        self.patcher.stop()
