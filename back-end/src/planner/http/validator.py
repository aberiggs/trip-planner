import json
from src.planner.http.response import *

def header_validator(event, keys):
    headers = event['headers']
    missing_keys = set(keys)

    for key in keys:
        if key in headers:
            missing_keys.remove(key)
    
    if len(missing_keys) == 0:
        return None

    return response_handler(400, {
        "message": f"The following fields are missing in header: {', '.join(sorted(list(missing_keys)))}"
    })


def post_body_validator(event, keys):
    body = json.loads(event["body"])
    missing_keys = set(keys)

    for key in keys:
        if key in body:
            missing_keys.remove(key)
    
    if len(missing_keys) == 0:
        return None

    return response_handler(400, {
        "message": f"The following fields are missing in body: {', '.join(sorted(list(missing_keys)))}"
    })