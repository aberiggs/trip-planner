"""Module providing unit tests for response handler"""

from unittest import TestCase
from http import HTTPStatus
import pytest
from planner.http.response import response_handler


class TestResponse(TestCase):
    """Class containing all unit tests for response handler"""

    def setUp(self) -> None:
        pass

    def test_response_handler_normal(self) -> None:
        """Function that tests whether response handler won't raise any exception
        when response is normal"""

        response = {
            "code": HTTPStatus.OK.value,
            "body": {"message": "fake response"},
        }

        try:
            response_handler(response)
        except Exception as e:
            pytest.fail(f"response_handler raised an exception: {e}")

    def test_response_handler_without_code(self) -> None:
        """Function that tests whether response handler catches the missing key: code"""

        response = {"body": {"message": "fake response"}}

        with pytest.raises(ValueError):
            response_handler(response)

    def test_response_handler_without_body(self) -> None:
        """Function that tests whether response handler catches the missing key: body"""

        response = {"code": HTTPStatus.OK.value}

        with pytest.raises(ValueError):
            response_handler(response)

    def tearDown(self) -> None:
        pass
