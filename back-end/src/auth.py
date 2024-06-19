import json
from google.oauth2.id_token import verify_oauth2_token
from google.auth.transport import requests
from src.planner.util.get_secret import get_secret
from src.planner.http.validator import post_body_validator
from src.planner.http.response import response_handler
from src.planner.jwt.create_jwt_token import *

WEB_CLIENT_ID = get_secret("auth", "web_client_id")
IOS_CLIENT_ID = get_secret("auth", "ios_client_id")


def lambda_handler(event, context):
    body = json.loads(event["body"])
    body_validator_response = post_body_validator(event, ["id_token", "client_type"])
    
    if body_validator_response is not None:
        return body_validator_response
    
    id_token = body["id_token"]
    client_type = body["client_type"]

    try:
        if client_type == "web":
            id_info = verify_oauth2_token(id_token, requests.Request(), WEB_CLIENT_ID)
        elif client_type == "ios":
            id_info = verify_oauth2_token(id_token, requests.Request(), IOS_CLIENT_ID)
        else:
            raise ValueError

        token_payload = {
            "email": id_info["email"],
            "picture": id_info["picture"],
            "name": id_info["name"]
        }

        jwt_token = create_jwt_token(token_payload)
        return response_handler(200, { "jwt": jwt_token })

    except ValueError:
        return response_handler(401, { "message": "invalid idToken" })