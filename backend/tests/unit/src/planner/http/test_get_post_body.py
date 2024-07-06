"""Module providing unit tests for http validator"""

import json
from unittest import TestCase
from http import HTTPStatus
import pytest
from planner.http.validator import header_validator, get_post_body
from planner.http.exception import HttpException


class TestValidator(TestCase):
    """Class containing all unit tests for http validator"""

    def setUp(self) -> None:
        pass

    def test_header_validator_missing_header(self) -> None:
        """Function that tests whether header validator catches the missing header"""

        expected_keys = ["Authentication", "Content-Type"]

        event = {"headers": {"Content-Type": "application/json"}}

        with pytest.raises(HttpException) as e:
            header_validator(event, expected_keys)
            assert e.args[0] == {
                "code": HTTPStatus.BAD_REQUEST.value,
                "body": {
                    "message": "The following fields are missing in header: Authentication"
                },
            }

    def test_header_validator_missing_headers(self) -> None:
        """Function that tests whether header validator catches missing headers"""

        expected_keys = ["Authentication", "Content-Type"]

        event = {"headers": {}}

        missing_keys = ", ".join(
            sorted(list(["Authentication", "Content-Type"]))
        )

        with pytest.raises(HttpException) as e:
            header_validator(event, expected_keys)
            assert e.args[0] == {
                "code": HTTPStatus.BAD_REQUEST.value,
                "body": {
                    "message": f"The following fields are missing in header: {missing_keys}"
                },
            }

    def test_header_validator_no_missing_header(self) -> None:
        """Function that tests whether header validator returns None when there are
        no missing headers"""

        expected_keys = ["Authentication"]

        event = {"headers": {"Authentication"}}

        try:
            header_validator(event, expected_keys)
        except Exception as e:
            pytest.fail(f"header_validator raised an exception: {e}")

    def test_post_body_validator_missing_key(self) -> None:
        """Function that tests whether get_post_body catches the missing key"""

        expected_keys = ["name", "email", "addr"]

        event = {
            "headers": {},
            "body": json.dumps(
                {"name": "willy", "email": "chiweilien@gmail.com"}
            ),
        }

        with pytest.raises(HttpException) as e:
            get_post_body(event, expected_keys)
            assert e.args[0] == {
                "code": HTTPStatus.BAD_REQUEST.value,
                "body": {
                    "message": "The following fields are missing in body: addr"
                },
            }

    def test_post_body_validator_missing_keys(self) -> None:
        """Function that tests whether get_post_body catches missing keys"""

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

        with pytest.raises(HttpException) as e:
            get_post_body(event, expected_keys)
            assert e.args[0] == {
                "code": HTTPStatus.BAD_REQUEST.value,
                "body": {
                    "message": f"The following fields are missing in body: {missing_keys}"
                },
            }

    def test_post_body_validator_no_missing_keys(self) -> None:
        """Function that tests whether get_post_body returns None when there
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
        try:
            get_post_body(event, expected_keys)
        except Exception as e:
            pytest.fail(f"post_body_validator raised an exception: {e}")

    def tearDown(self) -> None:
        pass
