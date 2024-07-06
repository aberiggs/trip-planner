"""Module providing integration test for creating plan with valid body"""

import json
from bson.objectid import ObjectId
from planner.db.serialize.jsonify_plan import jsonify_plan


def test_create_plan(
        patch_get_session_repos,
        user_repo,
        plan_repo,
        user,
        plan_info
    ):
    """Function that tests whether create_plan create plan properly with valid body"""

    from plan.create_plan import lambda_handler
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

    event = {
        "headers": {"Authorization": f"Bearer {jwt_token}"},
        "body": json.dumps(plan_info),
    }

    lambda_response = lambda_handler(event, None)

    result = json.loads(lambda_response["body"])
    found_plan = plan_repo.find_one_by_id(ObjectId(result["plan_id"]))

    updated_user = user_repo.find_one_by_id(user["_id"])
    assert found_plan["_id"] in updated_user["plans"]
    assert jsonify_plan(found_plan) == result
