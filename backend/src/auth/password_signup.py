"""Module providing the handler for password sign up endpoint"""

import json
from http import HTTPStatus
from planner.http.validator import post_body_validator
from planner.http.response import response_handler
from planner.db.repo.user_repo import UserRepo
from planner.db.db_init import db_init
from planner.util.password import hash_password
from planner.http.exception import HttpException, EmailUsedException


def db_setup():
    """Function thaht sets up mongodb client, session, schema enforcement"""

    client, session = db_init()
    db = client.trip_planner
    user_repo = UserRepo(db, session)
    return user_repo


def lambda_handler(event, context):
    """Lambda handler that signs up the user with email and password"""

    from planner.jwt.create_jwt_token import create_jwt_token
    from planner.util.get_utc_now import get_utc_now

    user_repo = db_setup()

    try:
        body = json.loads(event["body"])

        body_validator_response = post_body_validator(
            event, ["password", "first_name", "last_name", "email"]
        )
        if body_validator_response is not None:
            return body_validator_response

        utc_now = get_utc_now()
        first_name = body["first_name"]
        last_name = body["last_name"]
        email = body["email"]
        password = body["password"]
        hashed_salted_password = hash_password(password)

        if not user_repo.find_one_by_email(body["email"]):
            print("[info] user doesn't exist, signing up")
            user = {
                "first_name": first_name,
                "last_name": last_name,
                "picture": "",
                "email": email,
                "google_signup": False,
                "password": hashed_salted_password,
                "last_visited": utc_now,
                "plans": [],
            }
            user_repo.insert_one(user)
        else:
            raise EmailUsedException

        token_payload = {
            "email": email,
            "picture": "",
            "name": f"{first_name} {last_name}",
        }

        jwt_token = create_jwt_token(token_payload)
        return response_handler(
            {"code": HTTPStatus.OK, "body": {"jwt": jwt_token}}
        )

    except HttpException as e:
        return response_handler(e.args[0])
