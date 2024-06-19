import json
from google.oauth2 import id_token
from google.auth.transport import requests
from planner.util.get_secret import get_secret
from planner.http.validator import post_body_validator
from planner.http.response import response_handler
from planner.jwt.create_jwt_token import *

WEB_CLIENT_ID = get_secret("auth", "web_client_id")
IOS_CLIENT_ID = get_secret("auth", "ios_client_id")


def lambda_handler(event, context):
    body = json.loads(event["body"])
    body_validator_response = post_body_validator(event, ["id_token", "client_type"])
    
    if body_validator_response is not None:
        return body_validator_response
    
    idToken = body["id_token"]
    client_type = body["client_type"]

    try:
        # verify token turned off for testing
        # if client_type == "web":
        #     idinfo = id_token.verify_oauth2_token(idToken, requests.Request(), WEB_CLIENT_ID)
        # elif client_type == "ios":
        #     idinfo = id_token.verify_oauth2_token(idToken, requests.Request(), IOS_CLIENT_ID)

        # token_payload = {
        #     "email": idinfo["email"],
        #     "picture": idinfo["picture"],
        #     "name": idinfo["name"]
        # }

        token_payload = {
            "email": "chiweilien@gmail.com",
            "picture": "mypicture",
            "name": "Chi-Wei Lien"
        }
        jwt_token = create_jwt_token(token_payload)
        return response_handler(200, { "jwt": jwt_token })

    except ValueError:
        return response_handler(401, { "message": "invalid idToken" })