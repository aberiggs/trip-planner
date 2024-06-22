from unittest import TestCase
from src.planner.http.validator import header_validator, post_body_validator
from src.planner.http.response import *
from unittest.mock import patch

class TestValidator(TestCase):
    def setUp(self) -> None:
        mock_id_info = {
            "email": "hello@gmail.com",
            "picture": "picture.url",
            "name": "hello"
        }
        self.google_id_token_patcher = patch("google.oauth2.id_token.verify_oauth2_token", return_value=mock_id_info) 
        self.google_id_token_patcher.start()

        self.secret_patcher = patch('src.planner.util.get_secret.get_secret', return_value='mock_secret') 
        self.secret_patcher.start()

        self.jwt_token_patcher = patch("src.planner.jwt.create_jwt_token.create_jwt_token", return_value="mock token") 
        self.jwt_token_patcher.start()

    def test_auth_valid_body(self) -> None:
        from src.planner.jwt.create_jwt_token import create_jwt_token
        from src.auth import lambda_handler

        event = {
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "id_token": "mock token",
                "client_type": "web"
            })
        }

        jwt_token = create_jwt_token({})
        assert lambda_handler(event, None) == response_handler(200, { "jwt": jwt_token })

    def test_auth_no_id_token(self) -> None:
        from src.planner.jwt.create_jwt_token import create_jwt_token
        from src.auth import lambda_handler

        event = {
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "client_type": "web"
            })
        }

        assert lambda_handler(event, None) == response_handler(400, {
            "message": f"The following fields are missing in body: id_token"
        })
    
    def test_auth_no_client_type(self) -> None:
        from src.planner.jwt.create_jwt_token import create_jwt_token
        from src.auth import lambda_handler

        event = {
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "id_token": "mock token",
            })
        }

        assert lambda_handler(event, None) == response_handler(400, {
            "message": f"The following fields are missing in body: client_type"
        })

    def test_auth_invalid_client_type(self) -> None:
        from src.planner.jwt.create_jwt_token import create_jwt_token
        from src.auth import lambda_handler

        event = {
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "id_token": "mock token",
                "client_type": "hehe"
            })
        }

        assert lambda_handler(event, None) == response_handler(401, {
            "message": "invalid idToken"
        })


    def tearDown(self) -> None:
        self.google_id_token_patcher.stop()
        self.secret_patcher.stop()
        self.jwt_token_patcher.stop()