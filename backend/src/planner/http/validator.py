"""Module providing validator for HTTP requests (headers, POST body)"""

import json
from http import HTTPStatus
from planner.http.exception import HttpException
from planner.http.exception import InvalidBodyException


def header_validator(event, keys):
    """Function validating request headers"""

    headers = event["headers"]
    missing_keys = set(keys)

    for key in keys:
        if key in headers:
            missing_keys.remove(key)

    if len(missing_keys) == 0:
        return None

    missing_keys = ", ".join(sorted(list(missing_keys)))

    raise HttpException(
        {
            "code": HTTPStatus.BAD_REQUEST,
            "body": {
                "message": f"The following fields are missing in header: {missing_keys}"
            },
        }
    )


def get_post_body(event, keys):
    """Function validating POST request body"""

    try:
        body = json.loads(event["body"])
    except json.JSONDecodeError as e:
        raise InvalidBodyException from e

    missing_keys = set(keys)

    for key in keys:
        if key in body:
            missing_keys.remove(key)

    if len(missing_keys) == 0:
        return body

    missing_keys = ", ".join(sorted(list(missing_keys)))

    raise HttpException(
        {
            "code": HTTPStatus.BAD_REQUEST,
            "body": {
                "message": f"The following fields are missing in body: {missing_keys}"
            },
        }
    )
