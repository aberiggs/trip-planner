"""Module providing the handler for password sign up endpoint"""

import json
from planner.http.validator import post_body_validator
from planner.http.response import response_handler
from planner.http.error import INVALID_BODY, EMAIL_USED
from planner.db.user_schema import enforce_user_schema
from planner.db.create_collection import create_collection
from planner.db.db_init import db_init
import bcrypt


def db_setup():
    """Function thaht sets up mongodb client, session, schema enforcement"""
    client, session = db_init()
    db = client.trip_planner
    create_collection(db, "users")
    enforce_user_schema(db)
    return db, session


def lambda_handler(event, context):
    """Lambda handler that signs up the user with email and password"""

    from planner.jwt.create_jwt_token import create_jwt_token
    from planner.util.get_utc_now import get_utc_now

    db, session = db_setup()

    try:
        body = json.loads(event["body"])
    except json.JSONDecodeError:
        return INVALID_BODY

    body_validator_response = post_body_validator(
        event, ["password", "first_name", "last_name", "email"]
    )
    if body_validator_response is not None:
        return body_validator_response

    user_query = {"email": body["email"]}
    utc_now = get_utc_now()
    first_name = body["first_name"]
    last_name = body["last_name"]
    email = body["email"]
    password = body["password"]
    salt = bcrypt.gensalt()
    hashed_salted_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    if db.users.find_one(user_query, session=session) is None:
        print("[info] user doesn't exist, signing up")
        user = {
            "first_name": first_name,
            "last_name": last_name,
            "picture": "",
            "email": email,
            "google_login": False,
            "password": hashed_salted_password,
            "last_visited": utc_now,
            "plans": [],
        }
        db.users.insert_one(user, session=session)
        user_query = {"email": email}
    else:
        return EMAIL_USED

    token_payload = {
        "email": email,
        "picture": "",
        "name": f"{first_name} {last_name}",
    }

    jwt_token = create_jwt_token(token_payload)
    return response_handler(200, {"jwt": jwt_token})
