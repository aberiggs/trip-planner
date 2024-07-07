"""Module providing integration test for deleting plan"""

import json
from planner.date.get_plan_date import get_plan_date
from planner.http.response import handle_response
from planner.http.exception import ForbiddenException
from planner.date.get_activity_date import get_activity_date
from planner.db.serialize.jsonify_plan import jsonify_expanded_plan

def test_get_plan(
        patch_get_session_repos,
        user_repo,
        plan_repo,
        activity_repo,
        user,
        user2,
        activity_info,
        plan_info
    ):
    """Function that tests whether get_plan get plan properly"""

    from plan.get_plan import lambda_handler
    from plan.get_plan import expand_plan
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
        "owner": user["_id"],
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

    plan_repo.update_one_by_id(
        plan["_id"],
        {
            "$push": {
                "activities": activity["_id"]
            }
        }
    )

    user_repo.update_one_by_id(
        user["_id"],
        {
            "$push": {
                "plans": plan["_id"]
            }
        }
    )

    updated_plan = plan_repo.find_one_by_id(plan["_id"])
    assert updated_plan
    assert activity_repo.find_one_by_id(activity["_id"])

    event = {
        "headers": {"Authorization": f"Bearer {jwt_token}"},
        "pathParameters": { "plan_id": str(plan["_id"])},
    }

    lambda_response = lambda_handler(event, None)
    result = json.loads(lambda_response["body"])
    assert result == jsonify_expanded_plan(expand_plan(updated_plan, user_repo, activity_repo))

def test_get_plan_user_not_member(
        patch_get_session_repos,
        user_repo,
        plan_repo,
        activity_repo,
        user,
        user2,
        activity_info,
        plan_info
    ):
    """Function that tests whether get_plan catches cases where user trying to get
    plans they are not part of"""

    from plan.get_plan import lambda_handler
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

    plan_repo.update_one_by_id(
        plan["_id"],
        {
            "$push": {
                "activities": activity["_id"]
            }
        }
    )

    updated_plan = plan_repo.find_one_by_id(plan["_id"])
    assert updated_plan
    assert activity_repo.find_one_by_id(activity["_id"])

    event = {
        "headers": {"Authorization": f"Bearer {jwt_token}"},
        "pathParameters": { "plan_id": str(plan["_id"])},
    }

    lambda_response = lambda_handler(event, None)

    assert lambda_response == handle_response(
        ForbiddenException().args[0]
    )

# def test_member_delete_plan(
#         patch_get_session_repos,
#         user_repo,
#         plan_repo,
#         user,
#         user2,
#         plan_info
#     ):
#     """Function that tests whether delete_plan catches cases where member trying
#     to delete plan"""

#     from plan.delete_plan import lambda_handler
#     from planner.jwt.create_jwt_token import create_jwt_token

#     user_repo.insert_one(user)
#     user_repo.insert_one(user2)

#     assert user_repo.find_one_by_id(user["_id"])

#     first_name = user["first_name"]
#     last_name = user["last_name"]

#     jwt_token = create_jwt_token(
#         {
#             "email": user["email"],
#             "picture": "",
#             "name": f"{first_name} {last_name}",
#         }
#     )

#     plan = {
#         "name": plan_info["name"],
#         "date": get_plan_date(plan_info["date"]),
#         "owner": user2["_id"],
#         "members": [user["_id"], user2["_id"]],
#         "activities": []
#     }

#     plan_repo.insert_one(plan)

#     assert plan_repo.find_one_by_id(plan["_id"])

#     event = {
#         "headers": {"Authorization": f"Bearer {jwt_token}"},
#         "body": json.dumps({"plan_id": str(plan["_id"])}),
#     }

#     lambda_response = lambda_handler(event, None)

#     assert lambda_response == handle_response(
#         ForbiddenException().args[0]
#     )
