"""Module providing integration test for getting plans"""

import json
from planner.date.get_plan_date import get_plan_date
from planner.db.serialize.jsonify_plan import jsonify_plan

def test_update_plan_valid_body(
        patch_get_session_repos,
        user_repo,
        plan_repo,
        user,
        user2,
        plan_info,
        plan_info2
    ):
    """Function that tests whether update_plan create plan properly with valid body"""

    from plan.get_plans import lambda_handler
    from planner.jwt.create_jwt_token import create_jwt_token

    user_repo.insert_one(user)
    user_repo.insert_one(user2)

    plan = {
        "name": plan_info["name"],
        "date": get_plan_date(plan_info["date"]),
        "owner": user["_id"],
        "members": [user["_id"]],
    }

    plan2 = {
        "name": plan_info2["name"],
        "date": get_plan_date(plan_info2["date"]),
        "owner": user2["_id"],
        "members": [user2["_id"], user["_id"]],
    }

    plan_repo.insert_one(plan)
    plan_repo.insert_one(plan2)

    user_repo.update_one_by_id(user["_id"], {"$push": {"plans": plan["_id"]}})

    user_repo.update_one_by_id(user["_id"], {"$push": {"plans": plan2["_id"]}})

    first_name = user["first_name"]
    last_name = user["last_name"]

    jwt_token = create_jwt_token(
        {
            "email": user["email"],
            "picture": "",
            "name": f"{first_name} {last_name}",
        }
    )

    event = {"headers": {"Authorization": f"Bearer {jwt_token}"}}

    lambda_response = lambda_handler(event, None)

    result = json.loads(lambda_response["body"])

    assert jsonify_plan(plan) in result
    assert jsonify_plan(plan2) in result
