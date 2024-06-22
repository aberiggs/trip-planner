"""Module providing the handler for authentication (sign in/up) endpoint"""

import json
import datetime
from google.oauth2.id_token import verify_oauth2_token
from google.auth.transport import requests
from planner.util.get_secret import get_secret
from planner.http.validator import post_body_validator
from planner.http.response import response_handler
from planner.jwt.create_jwt_token import create_jwt_token
from planner.db.user_schema import enforce_user_schema
from planner.db.create_collection import create_collection
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

WEB_CLIENT_ID = get_secret("auth", "web_client_id")
IOS_CLIENT_ID = get_secret("auth", "ios_client_id")

mongo_db_connect_url = get_secret(
    "mongo-db-connection-secret", "mongo_db_connect_url"
)
client = MongoClient(mongo_db_connect_url, server_api=ServerApi("1"))
db = client.trip_planner
create_collection(db, "users")
enforce_user_schema(db)


def lambda_handler(event, context):
    """Lambda handler that sign in or up the user"""

    body = json.loads(event["body"])
    body_validator_response = post_body_validator(
        event, ["id_token", "client_type"]
    )

    if body_validator_response is not None:
        return body_validator_response

    id_token = body["id_token"]
    client_type = body["client_type"]

    try:
        if client_type == "web":
            id_info = verify_oauth2_token(
                id_token, requests.Request(), WEB_CLIENT_ID
            )
        elif client_type == "ios":
            id_info = verify_oauth2_token(
                id_token, requests.Request(), IOS_CLIENT_ID
            )
        else:
            raise ValueError
    except ValueError:
        return response_handler(401, {"message": "invalid idToken"})

    user_query = {"email": id_info["email"]}
    utc_now = datetime.datetime.now(tz=datetime.timezone.utc)

    if db.users.find_one(user_query) is None:
        print("[info] user doesn't exist, signing up")
        user = {
            "first_name": id_info["given_name"],
            "last_name": id_info["family_name"],
            "picture": id_info["picture"],
            "email": id_info["email"],
            "last_visited": utc_now,
            "plans": [],
        }
        db.users.insert_one(user)
    else:
        print("[info] user exists, signing in")
        db.users.update_one(
            user_query,
            {
                "$set": {
                    "first_name": id_info["given_name"],
                    "last_name": id_info["family_name"],
                    "picture": id_info["picture"],
                    "last_visited": utc_now,
                }
            },
        )

    token_payload = {
        "email": id_info["email"],
        "picture": id_info["picture"],
        "name": id_info["name"],
    }

    jwt_token = create_jwt_token(token_payload)
    return response_handler(200, {"jwt": jwt_token})
