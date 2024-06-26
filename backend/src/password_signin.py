"""Module providing the handler for password sign in endpoint"""

import json
from http import HTTPStatus
from planner.http.validator import post_body_validator
from planner.http.response import response_handler
from planner.http.error import (
    INVALID_BODY,
    USER_NOT_EXIST,
    PASSWORD_INCORRECT,
)
from planner.db.user_schema import enforce_user_schema
from planner.db.create_collection import create_collection
from planner.db.db_init import db_init
from planner.util.password import check_password


def db_setup():
    """Function thaht sets up mongodb client, session, schema enforcement"""
    client, session = db_init()
    db = client.trip_planner
    create_collection(db, "users")
    enforce_user_schema(db)
    return db, session


def lambda_handler(event, context):
    """Lambda handler that signs in the user with email and password"""

    from planner.jwt.create_jwt_token import create_jwt_token
    from planner.util.get_utc_now import get_utc_now

    db, session = db_setup()

    try:
        body = json.loads(event["body"])
    except json.JSONDecodeError:
        return INVALID_BODY

    body_validator_response = post_body_validator(event, ["password", "email"])
    if body_validator_response is not None:
        return body_validator_response

    user_query = {"email": body["email"]}
    utc_now = get_utc_now()
    email = body["email"]
    password = body["password"]

    found_user = db.users.find_one(user_query, session=session)

    if found_user is None or found_user["google_signup"]:
        return USER_NOT_EXIST

    first_name = found_user["first_name"]
    last_name = found_user["last_name"]

    if check_password(password.encode("utf-8"), found_user["password"]):
        db.users.update_one(
            user_query,
            {
                "$set": {
                    "last_visited": utc_now,
                }
            },
            session=session,
        )

        token_payload = {
            "email": email,
            "picture": "",
            "name": f"{first_name} {last_name}",
        }

        jwt_token = create_jwt_token(token_payload)
        return response_handler(HTTPStatus.OK, {"jwt": jwt_token})

    return PASSWORD_INCORRECT
