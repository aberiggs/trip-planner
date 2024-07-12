"""Module providing the response handler"""

import json
from typing import Dict, Any


def handle_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Function that returns http reponse with CORS policy enabled"""

    if "code" not in response or "body" not in response:
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
