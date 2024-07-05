"""Module providing the handler for password sign in endpoint"""

import json
from http import HTTPStatus
from planner.http.validator import post_body_validator
from planner.http.response import response_handler
from planner.http.exception import (
    HttpException,
    PasswordIncorrectException,
    UserNotExistException,
    InvalidBodyException
)
from planner.db.repo.user_repo import UserRepo
from planner.db.db_init import db_init
from planner.util.password import check_password


def db_setup():
    """Function thaht sets up mongodb client, session, schema enforcement"""
    client, session = db_init()
    db = client.trip_planner
    user_repo = UserRepo(db, session)
    return user_repo


def lambda_handler(event, context):
    """Lambda handler that signs in the user with email and password"""

    from planner.jwt.create_jwt_token import create_jwt_token
    from planner.util.get_utc_now import get_utc_now

    user_repo = db_setup()

    try:
        try:
            body = json.loads(event["body"])
        except json.JSONDecodeError as e:
            raise InvalidBodyException from e

        post_body_validator(event, ["password", "email"])

        utc_now = get_utc_now()
        email = body["email"]
        password = body["password"]

        found_user = user_repo.find_one_by_email(email)

        if not found_user or found_user["google_signup"]:
            raise UserNotExistException

        first_name = found_user["first_name"]
        last_name = found_user["last_name"]

        if check_password(password.encode("utf-8"), found_user["password"]):
            user_repo.update_one(
                email,
                {
                    "$set": {
                        "last_visited": utc_now,
                    }
                },
            )

            jwt_token = create_jwt_token(
                {
                    "email": email,
                    "picture": "",
                    "name": f"{first_name} {last_name}",
                }
            )
            return response_handler(
                {"code": HTTPStatus.OK, "body": {"jwt": jwt_token}}
            )

        raise PasswordIncorrectException
    except HttpException as e:
        return response_handler(e.args[0])
