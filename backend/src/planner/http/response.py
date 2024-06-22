"""Module providing the response handler"""

import json


def response_handler(code, body):
    """Function that returns http reponse with CORS policy enabled"""

    return {
        "statusCode": code,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(body),
    }
