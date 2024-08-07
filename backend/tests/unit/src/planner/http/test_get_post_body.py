"""Module providing unit tests for http validators"""

import json
from http import HTTPStatus
import pytest
from planner.http.validator import validate_header, validate_get_post_body
from planner.http.exception import HttpException
from planner.http.exception import InvalidBodyException


def test_validate_header_missing_header() -> None:
    """Function that tests whether header validator catches the missing header"""

    expected_keys = ["Authentication", "Content-Type"]

    event = {"headers": {"Content-Type": "application/json"}}

    with pytest.raises(HttpException) as e:
        validate_header(event, expected_keys)
        assert e.args[0] == {
            "code": HTTPStatus.BAD_REQUEST.value,
            "body": {
                "message": "The following fields are missing in header: Authentication"
            },
        }


def test_validate_header_missing_headers() -> None:
    """Function that tests whether header validator catches missing headers"""

    expected_keys = ["Authentication", "Content-Type"]

    event = {"headers": {}}

    missing_keys = ", ".join(sorted(list(["Authentication", "Content-Type"])))

    with pytest.raises(HttpException) as e:
        validate_header(event, expected_keys)
        assert e.args[0] == {
            "code": HTTPStatus.BAD_REQUEST.value,
            "body": {
                "message": f"The following fields are missing in header: {missing_keys}"
            },
        }


def test_validate_header_no_missing_header() -> None:
    """Function that tests whether header validator returns None when there are
    no missing headers"""

    expected_keys = ["Authentication"]

    event = {"headers": {"Authentication"}}

    try:
        validate_header(event, expected_keys)
    except Exception as e:
        pytest.fail(f"validate_header raised an exception: {e}")


def test_post_body_validator_missing_key() -> None:
    """Function that tests whether get_post_body catches the missing key"""

    expected_keys = ["name", "email", "addr"]

    event = {
        "headers": {},
        "body": json.dumps({"name": "willy", "email": "chiweilien@gmail.com"}),
    }

    with pytest.raises(HttpException) as e:
        validate_get_post_body(event, expected_keys)
        assert e.args[0] == {
            "code": HTTPStatus.BAD_REQUEST.value,
            "body": {
                "message": "The following fields are missing in body: addr"
            },
        }


def test_validate_get_post_body_invalid_body() -> None:
    """Function that tests whether validate_get_post_body catches invalid body"""

    event = {
        "headers": {"Content-Type": "application/json"},
        # this body is missing a double quote
        "body": '{"id_token: "mock token", "client_type": "web"}',
    }

    with pytest.raises(HttpException) as e:
        validate_get_post_body(event, [])
        assert isinstance(e, InvalidBodyException)


def test_validate_get_post_body_missing_keys() -> None:
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
        validate_get_post_body(event, expected_keys)
        assert e.args[0] == {
            "code": HTTPStatus.BAD_REQUEST.value,
            "body": {
                "message": f"The following fields are missing in body: {missing_keys}"
            },
        }


def test_validate_post_body_validator_no_missing_keys() -> None:
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
        validate_get_post_body(event, expected_keys)
    except Exception as e:
        pytest.fail(f"post_body_validator raised an exception: {e}")
