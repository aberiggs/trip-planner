"""Module providing integration test for updating plan with valid body"""

import json
from unittest.mock import patch
from bson.objectid import ObjectId
import pytest
from planner.date.get_plan_date import get_plan_date
from planner.db.serialize.jsonify_plan import jsonify_plan
from planner.http.response import handle_response
from planner.http.exception import ForbiddenException

@pytest.fixture
def patch_db_setup(user_repo, plan_repo):
    """Function that provides fixture to patch db_setup so that transactions
    are properly rolled back at the end of the test"""

    with patch(
        "plan.update_plan.db_setup",
        return_value=[user_repo, plan_repo],
        autospec=True,
    ) as m:
        yield m


def test_update_plan(
        patch_db_setup,
        user_repo,
        plan_repo,
        user,
        plan_info
    ):
    """Function that tests whether update_plan create plan properly with valid body"""

    from plan.update_plan import lambda_handler
    from planner.jwt.create_jwt_token import create_jwt_token

    user_repo.insert_one(user)

    plan = {
        "name": plan_info["name"],
        "date": get_plan_date(plan_info["date"]),
        "owner": user["_id"],
        "members": [user["_id"]],
    }

    plan_repo.insert_one(plan)

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
        "body": json.dumps(
            {
                "plan_id": str(plan["_id"]),
                "name": "new name",
                "date": "09/30/22",
                "owner": str(user["_id"]),
                "members": [str(user["_id"])],
            }
        ),
    }

    lambda_response = lambda_handler(event, None)

    result = json.loads(lambda_response["body"])
    found_plan = plan_repo.find_one_by_id(ObjectId(result["plan_id"]))

    assert jsonify_plan(found_plan) == result


def test_update_plan_user_not_a_member(
        patch_db_setup,
        user_repo,
        plan_repo,
        user,
        user2,
        plan_info
    ):
    """Function that tests whether update_plan catches cases where a user trying
    to update a plan that they are not part of"""

    from plan.update_plan import lambda_handler
    from planner.jwt.create_jwt_token import create_jwt_token

    user_repo.insert_one(user)
    user_repo.insert_one(user2)

    plan = {
        "name": plan_info["name"],
        "date": get_plan_date(plan_info["date"]),
        "owner": user2["_id"],
        "members": [user2["_id"]],
    }

    plan_repo.insert_one(plan)

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
        "body": json.dumps(
            {
                "plan_id": str(plan["_id"]),
                "name": "new name",
                "date": "09/30/22",
                "owner": str(user["_id"]),
                "members": [str(user["_id"])],
            }
        ),
    }

    lambda_response = lambda_handler(event, None)

    assert lambda_response == handle_response(
        ForbiddenException().args[0]
    )

    # plan should remain unchanged
    assert plan_repo.find_one_by_id(plan["_id"]) == plan


def test_update_plan_user_not_owner(
        patch_db_setup,
        user_repo,
        plan_repo,
        user,
        user2,
        plan_info
    ):
    """Function that tests whether update_plan catches cases where member trying
    to modify the owner field of a plan"""

    from plan.update_plan import lambda_handler
    from planner.jwt.create_jwt_token import create_jwt_token

    user_repo.insert_one(user)
    user_repo.insert_one(user2)

    plan = {
        "name": plan_info["name"],
        "date": get_plan_date(plan_info["date"]),
        "owner": user2["_id"],
        "members": [user2["_id"], user["_id"]],
    }

    plan_repo.insert_one(plan)

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
        "body": json.dumps(
            {
                "plan_id": str(plan["_id"]),
                "name": "new name",
                "date": "09/30/22",
                "owner": str(user["_id"]),
                "members": [str(user["_id"])],
            }
        ),
    }

    lambda_response = lambda_handler(event, None)

    assert lambda_response == handle_response(
        ForbiddenException().args[0]
    )

    # plan should remain unchanged
    assert plan_repo.find_one_by_id(plan["_id"]) == plan
