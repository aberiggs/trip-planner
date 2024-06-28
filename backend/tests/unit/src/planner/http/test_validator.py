"""Module providing unit tests for http validator"""

import json
from unittest import TestCase
from http import HTTPStatus
from planner.http.validator import header_validator, post_body_validator
from planner.http.response import response_handler


class TestValidator(TestCase):
    """Class containing all unit tests for http validator"""

    def setUp(self) -> None:
        pass

    def test_header_validator_missing_header(self) -> None:
        """Function that tests whether header validator catches the missing header"""

        expected_keys = ["Authentication", "Content-Type"]

        event = {"headers": {"Content-Type": "application/json"}}
        assert header_validator(event, expected_keys) == response_handler(
            HTTPStatus.BAD_REQUEST,
            {
                "message": "The following fields are missing in header: Authentication"
            },
        )

    def test_header_validator_missing_headers(self) -> None:
        """Function that tests whether header validator catches missing headers"""

        expected_keys = ["Authentication", "Content-Type"]

        event = {"headers": {}}

        missing_keys = ", ".join(
            sorted(list(["Authentication", "Content-Type"]))
        )

        assert header_validator(event, expected_keys) == response_handler(
            HTTPStatus.BAD_REQUEST,
            {
                "message": f"The following fields are missing in header: {missing_keys}"
            },
        )

    def test_header_validator_no_missing_header(self) -> None:
        """Function that tests whether header validator returns None when there are
        no missing headers"""

        expected_keys = ["Authentication"]

        event = {"headers": {"Authentication"}}
        assert header_validator(event, expected_keys) is None

    def test_post_body_validator_missing_key(self) -> None:
        """Function that tests whether post body validator catches the missing key"""

        expected_keys = ["name", "email", "addr"]

        event = {
            "headers": {},
            "body": json.dumps(
                {"name": "willy", "email": "chiweilien@gmail.com"}
            ),
        }
        assert post_body_validator(event, expected_keys) == response_handler(
            HTTPStatus.BAD_REQUEST,
            {"message": "The following fields are missing in body: addr"},
        )

    def test_post_body_validator_missing_keys(self) -> None:
        """Function that tests whether post body validator catches missing keys"""

        expected_keys = ["name", "email", "addr"]

        event = {
            "headers": {},
            "body": json.dumps(
                {
                    "name": "willy",
                }
            ),
        }

        missing_keys = ", ".join(sorted(list(["email", "addr"])))

        assert post_body_validator(event, expected_keys) == response_handler(
            HTTPStatus.BAD_REQUEST,
            {
                "message": f"The following fields are missing in body: {missing_keys}"
            },
        )

    def test_post_body_validator_no_missing_keys(self) -> None:
        """Function that tests whether post body validator returns None when there
        are no missing keys"""

        expected_keys = ["name", "email", "addr"]

        event = {
            "headers": {},
            "body": json.dumps(
                {
                    "name": "willy",
                    "email": "chiweilien@gmail.com",
                    "addr": "my addr",
                }
            ),
        }
        assert post_body_validator(event, expected_keys) is None

    def tearDown(self) -> None:
        pass
