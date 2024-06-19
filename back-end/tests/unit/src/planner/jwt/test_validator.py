from unittest import TestCase
from unittest.mock import patch
import jwt
import time

class TestValidator(TestCase):
    def setUp(self) -> None:
        self.patcher = patch('src.planner.util.get_secret.get_secret', return_value='mock_secret') 
        self.patcher.start()

    def test_jwt_validator_signed_with_diff_secret(self) -> None:
        from src.planner.jwt.validator import jwt_validator

        payload = {
            "email": "chiweilien@gmail.com",
            "picture": "mypicture",
            "name": "Chi-Wei Lien"
        }

        current_time = int(time.time())
        expiration_time = current_time + 864000 # ten days

        token = jwt.encode(
            payload,
            'fake_secret',
            algorithm="HS256",
            headers={"exp": expiration_time}
        )

        assert jwt_validator(token) == False
    
    def test_jwt_validator_signed_with_same_secret(self) -> None:
        from src.planner.jwt.validator import jwt_validator

        payload = {
            "email": "chiweilien@gmail.com",
            "picture": "mypicture",
            "name": "Chi-Wei Lien"
        }

        current_time = int(time.time())
        expiration_time = current_time + 864000 # ten days

        token = jwt.encode(
            payload,
            'mock_secret',
            algorithm="HS256",
            headers={"exp": expiration_time}
        )

        assert jwt_validator(token) == True
    
    def test_jwt_validator_expired_jwt(self) -> None:
        from src.planner.jwt.validator import jwt_validator

        payload = {
            "email": "chiweilien@gmail.com",
            "picture": "mypicture",
            "name": "Chi-Wei Lien"
        }

        current_time = int(time.time())
        expiration_time = current_time - 10

        token = jwt.encode(
            payload,
            'mock_secret',
            algorithm="HS256",
            headers={"exp": expiration_time}
        )

        assert jwt_validator(token) == False
    
    def test_jwt_validator_no_exp(self) -> None:
        from src.planner.jwt.validator import jwt_validator

        payload = {
            "email": "chiweilien@gmail.com",
            "picture": "mypicture",
            "name": "Chi-Wei Lien"
        }

        token = jwt.encode(
            payload,
            'mock_secret',
            algorithm="HS256",
        )

        assert jwt_validator(token) == False


    def tearDown(self) -> None:
        self.patcher.stop()