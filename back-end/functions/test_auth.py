import json
import jwt
from util.get_secret import get_secret

SECRET_KEY = get_secret("auth", "jwt_secret_key")

def is_jwt_token_valid(jwtToken):
    try:
        jwt.decode(jwtToken, key=SECRET_KEY, algorithms=["HS256"])
        return True
    except Exception:
        return False


def lambda_handler(event, context):
    jwtToken = event['headers']['Authorization'].split(" ")[1].encode("utf-8")
    
    # TODO: check if token has expired

    if is_jwt_token_valid(jwtToken):
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "you are logged in",
            }),
        }

    return {
        "statusCode": 401,
        "body": json.dumps({
            "message": "you are not logged in",
        }),
    }