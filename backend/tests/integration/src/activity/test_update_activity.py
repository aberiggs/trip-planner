"""Module providing integration test for updating activity"""

import json
from bson.objectid import ObjectId
from planner.date.get_plan_date import get_plan_date
from planner.date.get_activity_date import get_activity_date
from planner.db.serialize.jsonify_activity import jsonify_activity
from planner.http.response import handle_response
from planner.http.exception import ForbiddenException

def test_update_activity(
        patch_get_session_repos,
        user_repo,
        plan_repo,
        activity_repo,
        user,
        user2,
        plan_info,
        activity_info
    ):
    """Function that tests whether update_activity updates activity properly"""

    from activity.create_activity import lambda_handler
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
        "members": [user["_id"], user2["_id"]],
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

    update_activity = {
        "name": "new name",
        "location": "new location",
        "start_time": activity_info["start_time"],
        "end_time" : activity_info["end_time"],
        "note": "new note",
        "plan_id": str(plan["_id"])
    }

    event = {
        "headers": {"Authorization": f"Bearer {jwt_token}"},
        "body": json.dumps(update_activity),
    }

    lambda_response = lambda_handler(event, None)
    result = json.loads(lambda_response["body"])
    found_activity = activity_repo.find_one_by_id(ObjectId(result["activity_id"]))
    assert jsonify_activity(found_activity) == result


def test_update_activity_user_not_member(
        patch_get_session_repos,
        user_repo,
        plan_repo,
        activity_repo,
        user,
        user2,
        plan_info,
        activity_info
    ):
    """Function that tests whether update_activity catches cases where user is
    not a member of the plan that the activity is part of"""

    from activity.create_activity import lambda_handler
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

    update_activity = {
        "name": "new name",
        "location": "new location",
        "start_time": activity_info["start_time"],
        "end_time" : activity_info["end_time"],
        "note": "new note",
        "plan_id": str(plan["_id"])
    }

    event = {
        "headers": {"Authorization": f"Bearer {jwt_token}"},
        "body": json.dumps(update_activity),
    }

    lambda_response = lambda_handler(event, None)

    assert lambda_response == handle_response(
        ForbiddenException().args[0]
    )

    # activity should remain unchanged
    assert activity_repo.find_one_by_id(activity["_id"]) == activity
