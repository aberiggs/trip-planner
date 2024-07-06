"""Module providing integration test for creating activity"""

import json
from planner.date.get_plan_date import get_plan_date
from planner.db.serialize.jsonify_activity import jsonify_activity
from bson.objectid import ObjectId

def test_create_activity(
        patch_get_session_repos,
        user_repo,
        plan_repo,
        activity_repo,
        user,
        plan_info,
        activity_info
    ):
    """Function that tests whether create_activity create activity properly"""

    from activity.create_activity import lambda_handler
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
        "start_time": activity_info["start_time"],
        "end_time": activity_info["end_time"],
        "note": activity_info["note"],
        "plan_id": str(plan["_id"])
    }

    event = {
        "headers": {"Authorization": f"Bearer {jwt_token}"},
        "body": json.dumps(activity),
    }

    lambda_response = lambda_handler(event, None)

    result = json.loads(lambda_response["body"])
    found_activity = activity_repo.find_one_by_id(ObjectId(result["activity_id"]))
    assert jsonify_activity(found_activity) == result
