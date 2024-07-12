"""Module providing integration test for signing in with password but signed up
with google"""

import json
from planner.http.response import handle_response
from planner.http.exception import UserNotExistException

def test_password_signin_google_signup(
    patch_get_utc_now,
    patch_get_session_repos,
    patch_create_jwt_token,
    patch_google_verify_token,
    patch_get_secret,
    mock_id_info,
    google_user,
    utc_now,
    user_repo,
):
    """Function that tests whether password_signin blocks users signed up with google"""

    from auth.password_signin import lambda_handler

    # Expecting the user exists in the database before the user sign in
    user_repo.insert_one(google_user)
    original_user = user_repo.find_one_by_email(mock_id_info["email"])
    assert original_user == google_user

    event = {
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "email": google_user["email"],
                "password": "",
            }
        ),
    }

    lambda_response = lambda_handler(event, None)
    updated_user = user_repo.find_one_by_email(mock_id_info["email"])

    # unsuccessful login should not update last_visited
    assert updated_user["last_visited"] == (utc_now).replace(tzinfo=None)
    assert lambda_response == handle_response(UserNotExistException().args[0])
