"""Module providing integration test for creating plan with valid body"""

import json
from unittest.mock import patch
from bson.objectid import ObjectId
import pytest
from planner.db.serialize.jsonify_plan import jsonify_plan

@pytest.fixture
def patch_db_setup(user_repo, plan_repo):
    """Function that provides fixture to patch db_setup so that transactions
    are properly rolled back at the end of the test"""

    with patch(
        "plan.create_plan.db_setup",
        return_value=[user_repo, plan_repo],
        autospec=True,
    ) as m:
        yield m


def test_create_plan(
        patch_db_setup,
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
