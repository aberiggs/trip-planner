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

    def test_jwt_extractor_normal(self) -> None:
        """Function that tests whether jwt validator catches token signed with a different key"""

        from planner.jwt.extractor import jwt_extractor
        from planner.jwt.create_jwt_token import create_jwt_token

        payload = {
            "email": "chiweilien@gmail.com",
            "picture": "mypicture",
            "name": "Chi-Wei Lien",
        }

        token = create_jwt_token(payload)
        assert jwt_extractor(token) == payload

    def test_jwt_extractor_signed_with_diff_secret(self) -> None:
        """Function that tests whether jwt extractor doesn't validate the token"""

        from planner.jwt.extractor import jwt_extractor

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
            extracted_payload = jwt_extractor(token)
        except Exception as e:
            pytest.fail(f"response_handler raised an exception: {e}")

        assert extracted_payload == payload

    def tearDown(self) -> None:
        self.patcher.stop()
