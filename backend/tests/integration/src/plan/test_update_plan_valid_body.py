"""Module providing integration test for updating plan with valid body"""

import json
import datetime
from unittest.mock import patch
from bson.objectid import ObjectId
import pytest
from planner.util.password import hash_password
from planner.date.get_plan_date import get_plan_date
from planner.db.serialize.plan_serializer import plan_serializer

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

plan_info = {
    "name": "steve's plan",
    "date": "09/19/22",
}


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


def test_update_plan_valid_body(patch_db_setup, user_repo, plan_repo):
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

    assert plan_serializer(found_plan) == result
