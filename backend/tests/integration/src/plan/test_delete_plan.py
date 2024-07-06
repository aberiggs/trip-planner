"""Module providing integration test for deleting plan"""

import json
from planner.date.get_plan_date import get_plan_date
from planner.http.response import handle_response
from planner.http.exception import ForbiddenException

def test_delete_plan(
        patch_get_session_repos,
        user_repo,
        plan_repo,
        user,
        user2,
        plan_info
    ):
    """Function that tests whether create_plan create plan properly with valid body"""

    from plan.delete_plan import lambda_handler
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
    }

    plan_repo.insert_one(plan)

    assert plan_repo.find_one_by_id(plan["_id"])

    event = {
        "headers": {"Authorization": f"Bearer {jwt_token}"},
        "body": json.dumps({"plan_id": str(plan["_id"])}),
    }

    lambda_handler(event, None)
    assert not plan_repo.find_one_by_id(plan["_id"])

    updated_user = user_repo.find_one_by_id(user["_id"])
    updated_user2 = user_repo.find_one_by_id(user["_id"])

    assert plan["_id"] not in updated_user["plans"]
    assert plan["_id"] not in updated_user2["plans"]


def test_member_delete_plan(
        patch_get_session_repos,
        user_repo,
        plan_repo,
        user,
        user2,
        plan_info
    ):
    """Function that tests whether delete_plan catches cases where member trying
    to delete plan"""

    from plan.delete_plan import lambda_handler
    from planner.jwt.create_jwt_token import create_jwt_token

    user_repo.insert_one(user)
    user_repo.insert_one(user2)

    assert user_repo.find_one_by_id(user["_id"])

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
    }

    plan_repo.insert_one(plan)

    assert plan_repo.find_one_by_id(plan["_id"])

    event = {
        "headers": {"Authorization": f"Bearer {jwt_token}"},
        "body": json.dumps({"plan_id": str(plan["_id"])}),
    }

    lambda_response = lambda_handler(event, None)

    assert lambda_response == handle_response(
        ForbiddenException().args[0]
    )
