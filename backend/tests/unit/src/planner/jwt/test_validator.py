"""Module providing unit tests for jwt validator"""

import time
from unittest import TestCase
from unittest.mock import patch
import jwt

class TestValidator(TestCase):
    """Class containing all unit tests for jwt validator"""

    def setUp(self) -> None:
        """Setup function that patches the result of
        planner.util.get_secret.get_secret to mock_secret"""

        self.patcher = patch(
            "planner.util.get_secret.get_secret", return_value="mock_secret"
        )
        self.patcher.start()

    def test_jwt_validator_signed_with_diff_secret(self) -> None:
        """Function that tests whether jwt validator catches token signed with a different key"""

        from planner.jwt.validator import jwt_validator

        payload = {
            "email": "chiweilien@gmail.com",
            "picture": "mypicture",
            "name": "Chi-Wei Lien",
        }

        current_time = int(time.time())
        expiration_time = current_time + 864000  # ten days

        token = jwt.encode(
            payload,
            "fake_secret",
            algorithm="HS256",
            headers={"exp": expiration_time},
        )

        assert jwt_validator(token) is False

    def test_jwt_validator_signed_with_same_secret(self) -> None:
        """Function that tests whether jwt validator returns true when token is
         signed with the same key"""

        from planner.jwt.validator import jwt_validator

        payload = {
            "email": "chiweilien@gmail.com",
            "picture": "mypicture",
            "name": "Chi-Wei Lien",
        }

        current_time = int(time.time())
        expiration_time = current_time + 864000  # ten days

        token = jwt.encode(
            payload,
            "mock_secret",
            algorithm="HS256",
            headers={"exp": expiration_time},
        )

        assert jwt_validator(token) is True

    def test_jwt_validator_expired_jwt(self) -> None:
        """Function that tests whether jwt validator catches expired token"""

        from planner.jwt.validator import jwt_validator

        payload = {
            "email": "chiweilien@gmail.com",
            "picture": "mypicture",
            "name": "Chi-Wei Lien",
        }

        current_time = int(time.time())
        expiration_time = current_time - 10

        token = jwt.encode(
            payload,
            "mock_secret",
            algorithm="HS256",
            headers={"exp": expiration_time},
        )

        assert jwt_validator(token) is False

    def test_jwt_validator_no_exp(self) -> None:
        """Function that tests whether jwt validator returns true when token
        hasn't expired"""

        from planner.jwt.validator import jwt_validator

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

        assert jwt_validator(token) is False

    def tearDown(self) -> None:
        self.patcher.stop()
