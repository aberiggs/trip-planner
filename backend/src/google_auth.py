"""Module providing the handler for google authentication (sign in/up) endpoint"""

import json
from http import HTTPStatus
from google.auth.transport import requests
from planner.util.get_secret import get_secret
from planner.http.validator import post_body_validator
from planner.http.response import response_handler
from planner.http.error import (
    INVALID_BODY,
    INVALID_GOOGLE_ID_TOKEN,
    INVALID_CLIENT_TYPE,
)
from planner.db.user_schema import enforce_user_schema
from planner.db.create_collection import create_collection
from planner.db.db_init import db_init

WEB_CLIENT_ID = get_secret("auth", "web_client_id")
IOS_CLIENT_ID = get_secret("auth", "ios_client_id")


def db_setup():
    """Function that sets up mongodb client, session, schema enforcement"""
    client, session = db_init()
    db = client.trip_planner
    create_collection(db, "users")
    enforce_user_schema(db)
    return db, session


def lambda_handler(event, context):
    """Lambda handler that signs in or up the user through Google"""

    from google.oauth2.id_token import verify_oauth2_token
    from planner.jwt.create_jwt_token import create_jwt_token
    from planner.util.get_utc_now import get_utc_now

    db, session = db_setup()

    try:
        body = json.loads(event["body"])
    except json.JSONDecodeError:
        return INVALID_BODY

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
            raise TypeError
    except ValueError:
        return INVALID_GOOGLE_ID_TOKEN
    except TypeError:
        return INVALID_CLIENT_TYPE

    user_query = {"email": id_info["email"]}
    utc_now = get_utc_now()
    first_name = id_info["given_name"]
    last_name = id_info["family_name"]
    picture = id_info["picture"]
    email = id_info["email"]

    if db.users.find_one(user_query, session=session) is None:
        print("[info] user doesn't exist, signing up")
        user = {
            "first_name": first_name,
            "last_name": last_name,
            "picture": picture,
            "email": email,
            "last_visited": utc_now,
            "google_login": True,
            "plans": [],
        }
        db.users.insert_one(user, session=session)
        user_query = {"email": email}
    else:
        print("[info] user exists, signing in")
        db.users.update_one(
            user_query,
            {
                "$set": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "picture": picture,
                    "last_visited": utc_now,
                }
            },
            session=session,
        )

    token_payload = {
        "email": email,
        "picture": picture,
        "name": f"{first_name} {last_name}",
    }

    jwt_token = create_jwt_token(token_payload)
    return response_handler(HTTPStatus.OK, {"jwt": jwt_token})
