"""Module providing validator for HTTP requests (headers, POST body)"""

import json
from planner.http.response import response_handler


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

    return response_handler(
        400,
        {
            "message": f"The following fields are missing in header: {missing_keys}"
        },
    )


def post_body_validator(event, keys):
    """Function validating POST request body"""

    body = json.loads(event["body"])
    missing_keys = set(keys)

    for key in keys:
        if key in body:
            missing_keys.remove(key)

    if len(missing_keys) == 0:
        return None

    missing_keys = ", ".join(sorted(list(missing_keys)))

    return response_handler(
        400,
        {
            "message": f"The following fields are missing in body: {missing_keys}"
        },
    )
