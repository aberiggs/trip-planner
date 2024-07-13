"""Module providing integration test for signing up with googe_auth"""

import json
from http import HTTPStatus
from planner.http.response import handle_response

def test_google_auth_signup(
    patch_get_utc_now,
    patch_get_session_repos,
    patch_create_jwt_token,
    patch_google_verify_token,
    patch_get_secret,
    mock_id_info,
    google_user,
    user_repo,
):
    """Function that tests whether auth properly sign up non-existing users"""

    from planner.jwt.create_jwt_token import create_jwt_token
    from auth.google_auth import lambda_handler

    event = {
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"id_token": "mock token", "client_type": "web"}),
    }

    assert not user_repo.find_one_by_email(mock_id_info["email"])

    jwt_token = create_jwt_token({})
    lambda_response = lambda_handler(event, None)

    new_user = user_repo.find_one_by_email(mock_id_info["email"])
    new_user.pop("_id")

    assert new_user == google_user
    assert lambda_response == handle_response(
        {"code": HTTPStatus.OK.value, "body": {"jwt": jwt_token}}
    )
