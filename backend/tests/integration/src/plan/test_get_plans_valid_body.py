"""Module providing integration test for updating plan with valid body"""

import json
import datetime
from unittest.mock import patch
import pytest
from planner.util.password import hash_password
from planner.date.get_plan_date import get_plan_date
from planner.db.serialize.jsonify_plan import jsonify_plan

utc_now = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)

user = {
    "first_name": "Steve",
    "last_name": "Bob",
    "picture": "steve.bob.png",
    "email": "steve.bob@email.com",
    "password": hash_password("steve's secure password"),
    "last_visited": utc_now.replace(tzinfo=None),
    "google_signup": False,
    "plans": [],
}

user2 = {
    "first_name": "Cool",
    "last_name": "Bob",
    "picture": "cool.bob.png",
    "email": "cool.bob@email.com",
    "password": hash_password("cool's secure password"),
    "last_visited": utc_now.replace(tzinfo=None),
    "google_signup": False,
    "plans": [],
}

plan_info = {
    "name": "steve's plan",
    "date": "09/19/22",
}

plan_info2 = {
    "name": "steve's second plan",
    "date": "09/20/22",
}


@pytest.fixture
def patch_db_setup(user_repo, plan_repo):
    """Function that provides fixture to patch db_setup so that transactions
    are properly rolled back at the end of the test"""

    with patch(
        "plan.get_plans.db_setup",
        return_value=[user_repo, plan_repo],
        autospec=True,
    ) as m:
        yield m


def test_update_plan_valid_body(patch_db_setup, user_repo, plan_repo):
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
