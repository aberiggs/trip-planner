"""Module providing the handler for update plan endpoint"""

import datetime
from http import HTTPStatus
from bson.objectid import ObjectId
from planner.http.validator import validate_get_post_body
from planner.middleware.check_user_signin import check_user_signin
from planner.jwt.extractor import extract_jwt
from planner.jwt.get_jwt_token import get_jwt_token
from planner.http.exception import (
    HttpException,
    ResourceNotFoundException,
    ForbiddenException,
)
from planner.http.response import handle_response

utc_now = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)

def lambda_handler(event, context):
    """Lambda handler that update a plan in the database"""
    from planner.db.repo.get_session_repos import get_session_repos

    repos = get_session_repos()
    user_repo = repos["user"]
    plan_repo = repos["plan"]
    activity_repo = repos["activity"]

    try:
        body = validate_get_post_body(event, ["plan_id"])
        check_user_signin(event)

        jwt_payload = extract_jwt(get_jwt_token(event))
        plan_id = ObjectId(body["plan_id"])

        curr_user = user_repo.find_one_by_email(jwt_payload["email"])
        if not curr_user:
            print("[error] curr user not found")
            raise ResourceNotFoundException

        plan = plan_repo.find_one_by_id(plan_id)
        if not plan:
            print("[error] given plan not found")
            raise ResourceNotFoundException

        # only owner can remove the plan
        if plan["owner"] != curr_user["_id"]:
            raise ForbiddenException

        # remove plan from members
        for member in plan["members"]:
            user_repo.update_one_by_id(
                member,
                {
                    "$set": {
                        "last_visited": utc_now,
                    },
                    "$pull": {"plans": plan_id},
                },
            )

        # remove all associated activities
        for activity in plan["activities"]:
            activity_repo.delete_one_by_id(activity)

        plan_repo.delete_one_by_id(plan_id)

        return handle_response(
            {
                "code": HTTPStatus.NO_CONTENT.value,
                "body": {"message": "plan deleted"},
            }
        )

    except HttpException as e:
        return handle_response(e.args[0])
