import json
from google.oauth2 import id_token
from google.auth.transport import requests
import time
import jwt
from util.get_secret import get_secret
from jwt import InvalidSignatureError

SECRET_KEY = get_secret("auth", "jwt_secret_key")
WEB_CLIENT_ID = get_secret("auth", "web_client_id")

def create_jwt_token(payload):
    current_time = int(time.time())
    expiration_time = current_time + 864000 # ten days

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256",
        headers={"exp": expiration_time}
    )

    return token

def is_jwt_token_valid(jwtToken):
    try:
        jwt.decode(jwtToken, key=SECRET_KEY, algorithms=["HS256"])
        return True
    except InvalidSignatureError:
        return False


def lambda_handler(event, context):
    body = json.loads(event["body"])
    idToken = body["idToken"]

    try:
        idinfo = id_token.verify_oauth2_token(idToken, requests.Request(), WEB_CLIENT_ID)

        token_payload = {
            "user_id": idinfo["sub"],
            "email": idinfo["email"],
            "picture": idinfo["picture"],
            "name": idinfo["name"]
        }
        jwt_token = create_jwt_token(token_payload)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps({
                "jwt": jwt_token
            }),
        }

    except ValueError:
        return {
            "statusCode": 401,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps({
                "message": "invalid idToken",
            }),
        }