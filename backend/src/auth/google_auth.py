"""Module providing the handler for google authentication (sign in/up) endpoint"""

from http import HTTPStatus
from google.auth.transport import requests
from planner.util.get_secret import get_secret
from planner.http.validator import validate_get_post_body
from planner.http.response import handle_response
from planner.http.exception import (
    HttpException,
    InvalidGoogleIdTokenException,
    InvalidClientTypeException,
    GoogleSignInFailedException,
)

WEB_CLIENT_ID = get_secret("auth", "web_client_id")
IOS_CLIENT_ID = get_secret("auth", "ios_client_id")


def lambda_handler(event, context):
    """Lambda handler that signs in or up the user through Google"""

    from google.oauth2.id_token import verify_oauth2_token
    from planner.jwt.create_jwt_token import create_jwt_token
    from planner.util.get_utc_now import get_utc_now
    from planner.db.repo.get_session_repos import get_session_repos

    repos = get_session_repos()
    user_repo = repos["user"]

    try:
        body = validate_get_post_body(event, ["id_token", "client_type"])

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
        except ValueError as e:
            raise InvalidGoogleIdTokenException from e
        except TypeError as e:
            raise InvalidClientTypeException from e

        utc_now = get_utc_now()

        first_name = id_info["given_name"]
        last_name = id_info["family_name"]
        picture = id_info["picture"]
        email = id_info["email"]

        found_user = user_repo.find_one_by_email(id_info["email"])

        if not found_user:
            print("[info] user doesn't exist, signing up")
            user_repo.insert_one(
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "picture": picture,
                    "email": email,
                    "last_visited": utc_now,
                    "google_signup": True,
                    "password": b"",
                    "plans": [],
                }
            )
        else:
            print("[info] user exists, signing in")

            if not found_user["google_signup"]:
                raise GoogleSignInFailedException

            user_repo.update_one_by_email(
                email,
                {
                    "$set": {
                        "first_name": first_name,
                        "last_name": last_name,
                        "picture": picture,
                        "last_visited": get_utc_now(),
                    }
                },
            )

        token_payload = {
            "email": email,
            "picture": picture,
            "name": f"{first_name} {last_name}",
        }

        jwt_token = create_jwt_token(token_payload)
        return handle_response(
            {"code": HTTPStatus.OK, "body": {"jwt": jwt_token}}
        )
    except HttpException as e:
        return handle_response(e.args[0])
