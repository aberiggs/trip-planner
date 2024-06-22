"""Module providing unit tests for the auth lambda handler"""

import json
from unittest import TestCase
from unittest.mock import patch
from planner.http.response import response_handler

class TestAuth(TestCase):
    """Class containing all unit tests for auth"""

    def setUp(self) -> None:
        """Setup function that patches the result of
        google.oauth2.id_token.verify_oauth2_token, planner.util.get_secret.get_secret,
        and planner.jwt.create_jwt_token.create_jwt_token"""

        mock_id_info = {
            "email": "hello@gmail.com",
            "picture": "picture.url",
            "name": "hello",
        }
        self.google_id_token_patcher = patch(
            "google.oauth2.id_token.verify_oauth2_token",
            return_value=mock_id_info,
        )
        self.google_id_token_patcher.start()

        self.secret_patcher = patch(
            "planner.util.get_secret.get_secret", return_value="mock_secret"
        )
        self.secret_patcher.start()

        self.jwt_token_patcher = patch(
            "planner.jwt.create_jwt_token.create_jwt_token",
            return_value="mock token",
        )
        self.jwt_token_patcher.start()

    def test_auth_valid_body(self) -> None:
        """Function that tests whether auth returns JWT token properly"""

        from planner.jwt.create_jwt_token import create_jwt_token
        from auth import lambda_handler

        event = {
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {"id_token": "mock token", "client_type": "web"}
            ),
        }

        jwt_token = create_jwt_token({})
        assert lambda_handler(event, None) == response_handler(
            200, {"jwt": jwt_token}
        )

    def test_auth_no_id_token(self) -> None:
        """Function that tests whether auth returns error when id_token is absent"""

        from auth import lambda_handler

        event = {
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"client_type": "web"}),
        }

        assert lambda_handler(event, None) == response_handler(
            400,
            {"message": "The following fields are missing in body: id_token"},
        )

    def test_auth_no_client_type(self) -> None:
        """Function that tests whether auth returns error when client_type is absent"""

        from auth import lambda_handler

        event = {
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {
                    "id_token": "mock token",
                }
            ),
        }

        assert lambda_handler(event, None) == response_handler(
            400,
            {
                "message": "The following fields are missing in body: client_type"
            },
        )

    def test_auth_invalid_client_type(self) -> None:
        """Function that tests whether auth returns error when client_type is invalid"""

        from auth import lambda_handler

        event = {
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {"id_token": "mock token", "client_type": "hehe"}
            ),
        }

        assert lambda_handler(event, None) == response_handler(
            401, {"message": "invalid idToken"}
        )

    def tearDown(self) -> None:
        self.google_id_token_patcher.stop()
        self.secret_patcher.stop()
        self.jwt_token_patcher.stop()
