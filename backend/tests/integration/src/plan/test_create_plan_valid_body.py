"""Module providing integration test for creating plan with valid body"""

import json
import datetime
from unittest.mock import patch
from bson.objectid import ObjectId
import pytest
from planner.util.password import hash_password
from planner.date.get_plan_date import get_plan_date

utc_now = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)

user_info = {
    "first_name": "Steve",
    "last_name": "Bob",
    "picture": "steve.bob.png",
    "email": "steve.bob@email.com",
    "password": hash_password("steve's secure password"),
    "last_visited": utc_now.replace(tzinfo=None),
    "google_signup": False,
    "plans": [],
}

plan_info = {
    "name": "steve's plan",
    "date": "09/19/22",
    "owner": "steve.bob@email.com"
}

@pytest.fixture
def patch_db_setup(user_repo, plan_repo):
    """Function that provides fixture to patch auth.db_setup so that transactions
    are properly rolled back at the end of the test"""

    with patch(
        "plan.create_plan.db_setup",
        return_value=[user_repo, plan_repo],
        autospec=True,
    ) as m:
        yield m

def test_create_plan_valid_body(
    patch_db_setup,
    user_repo,
    plan_repo
):
    """Function that tests whether password_signin blocks users signed up with google"""

    from plan.create_plan import lambda_handler
    from planner.jwt.create_jwt_token import create_jwt_token

    user_repo.insert_one(user_info)
    first_name = user_info["first_name"]
    last_name = user_info["last_name"]

    jwt_token = create_jwt_token(
        {
            "email": user_info["email"],
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
    result["_id"] = ObjectId(result["_id"])
    result["owner"] = ObjectId(result["owner"])
    result["date"] = get_plan_date(result["date"])

    assert plan_repo.find_one_by_id(ObjectId(result["_id"])) == result
