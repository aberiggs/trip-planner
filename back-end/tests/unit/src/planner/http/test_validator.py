from unittest import TestCase
from src.planner.http.validator import header_validator, post_body_validator
from src.planner.http.response import *

class TestValidator(TestCase):
    def setUp(self) -> None:
        pass

    def test_header_validator_missing_header(self) -> None:
        expected_keys = ['Authentication', 'Content-Type']

        event = {
            'headers': {
                'Content-Type': 'application/json'
            }
        }
        assert header_validator(event, expected_keys) == response_handler(400, {
            "message": f"The following fields are missing in header: Authentication"
        })

    def test_header_validator_missing_headers(self) -> None:
        expected_keys = ['Authentication', 'Content-Type']

        event = {
            'headers': {}
        }

        assert header_validator(event, expected_keys) == response_handler(400, {
            "message": f"The following fields are missing in header: {', '.join(sorted(list(['Authentication', 'Content-Type'])))}"
        })

    def test_header_validator_no_missing_header(self) -> None:
        expected_keys = ['Authentication']

        event = {
            'headers': {'Authentication'}
        }
        assert header_validator(event, expected_keys) == None


    def test_post_body_validator_missing_header(self) -> None:
        expected_keys = ['name', 'email', 'addr']

        event = {
            'headers': {},
            'body': json.dumps({
                'name': 'willy',
                'email': 'chiweilien@gmail.com'
            })
        }
        assert post_body_validator(event, expected_keys) == response_handler(400, {
            "message": f"The following fields are missing in body: addr"
        })

    def test_post_body_validator_missing_headers(self) -> None:
        expected_keys = ['name', 'email', 'addr']

        event = {
            'headers': {},
            'body': json.dumps({
                'name': 'willy',
            })
        }
        assert post_body_validator(event, expected_keys) == response_handler(400, {
            "message": f"The following fields are missing in body: {', '.join(sorted(list(['email', 'addr'])))}"
        })

    def test_post_body_validator_missing_headers(self) -> None:
        expected_keys = ['name', 'email', 'addr']

        event = {
            'headers': {},
            'body': json.dumps({
                'name': 'willy',
                'email': 'chiweilien@gmail.com',
                'addr': 'my addr'
            })
        }
        assert post_body_validator(event, expected_keys) == None

    def tearDown(self) -> None:
        pass