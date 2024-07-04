"""Module providing the response handler"""

import json
from typing import Dict, Any


def response_handler(response: Dict[str, Any]) -> Dict[str, Any]:
    """Function that returns http reponse with CORS policy enabled"""

    if "code" in response and "body" not in response:
        raise ValueError(
            "Invalid response format. Expected a response dict with 'code' and 'body' keys."
        )

    return {
        "statusCode": response["code"],
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(response["body"]),
    }
