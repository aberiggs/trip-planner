"""Module providing integration test for deleting activity"""

import json
from http import HTTPStatus
from planner.date.get_plan_date import get_plan_date
from planner.date.get_activity_date import get_activity_date
from planner.http.response import handle_response
from planner.http.exception import ForbiddenException

def test_delete_activity(
        patch_get_session_repos,
        user_repo,
        plan_repo,
        activity_repo,
        user,
        plan_info,
        activity_info
    ):
    """Function that tests whether delete_activity deletes activity properly"""

    from activity.delete_activity import lambda_handler
    from planner.jwt.create_jwt_token import create_jwt_token

    user_repo.insert_one(user)
    first_name = user["first_name"]
    last_name = user["last_name"]

    jwt_token = create_jwt_token(
        {
            "email": user["email"],
            "picture": "",
            "name": f"{first_name} {last_name}",
        }
    )

    plan = {
        "name": plan_info["name"],
        "date": get_plan_date(plan_info["date"]),
        "owner": user["_id"],
        "members": [user["_id"]],
        "activities": []
    }
    plan_repo.insert_one(plan)

    activity = {
        "name": activity_info["name"],
        "location": activity_info["location"],
        "start_time": get_activity_date(activity_info["start_time"]),
        "end_time": get_activity_date(activity_info["end_time"]),
        "note": activity_info["note"],
        "plan_id": plan["_id"]
    }
    activity_repo.insert_one(activity)

    event = {
        "headers": {"Authorization": f"Bearer {jwt_token}"},
        "body": json.dumps({
            "activity_id": str(activity["_id"])
        }),
    }

    lambda_response = lambda_handler(event, None)

    assert lambda_response["statusCode"] == HTTPStatus.NO_CONTENT

    assert not activity_repo.find_one_by_id(activity["_id"])

    updated_plan = plan_repo.find_one_by_id(plan["_id"])
    assert activity["_id"] not in updated_plan["activities"]


def test_delete_activity_user_not_member(
        patch_get_session_repos,
        user_repo,
        plan_repo,
        activity_repo,
        user,
        user2,
        plan_info,
        activity_info
    ):
    """Function that tests whether delete_activity delete activity properly"""

    from activity.delete_activity import lambda_handler
    from planner.jwt.create_jwt_token import create_jwt_token

    user_repo.insert_one(user)
    user_repo.insert_one(user2)
    first_name = user["first_name"]
    last_name = user["last_name"]

    jwt_token = create_jwt_token(
        {
            "email": user["email"],
            "picture": "",
            "name": f"{first_name} {last_name}",
        }
    )

    plan = {
        "name": plan_info["name"],
        "date": get_plan_date(plan_info["date"]),
        "owner": user2["_id"],
        "members": [user2["_id"]],
        "activities": []
    }
    plan_repo.insert_one(plan)

    activity = {
        "name": activity_info["name"],
        "location": activity_info["location"],
        "start_time": get_activity_date(activity_info["start_time"]),
        "end_time": get_activity_date(activity_info["end_time"]),
        "note": activity_info["note"],
        "plan_id": plan["_id"]
    }
    activity_repo.insert_one(activity)

    event = {
        "headers": {"Authorization": f"Bearer {jwt_token}"},
        "body": json.dumps({
            "activity_id": str(activity["_id"])
        }),
    }

    lambda_response = lambda_handler(event, None)

    assert lambda_response == handle_response(
        ForbiddenException().args[0]
    )

    assert plan_repo.find_one_by_id(plan["_id"]) == plan
