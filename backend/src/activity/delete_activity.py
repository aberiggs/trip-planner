"""Module providing the handler for activity creation"""

from http import HTTPStatus
from bson.objectid import ObjectId
from planner.http.validator import validate_get_post_body
from planner.middleware.check_user_signin import check_user_signin
from planner.http.response import handle_response
from planner.http.exception import (
    HttpException,
    ResourceNotFoundException,
    ForbiddenException
)
from planner.jwt.extractor import extract_jwt
from planner.jwt.get_jwt_token import get_jwt_token


def lambda_handler(event, context):
    """Lambda handler that creates an activity document in MongoDB"""
    from planner.db.repo.get_session_repos import get_session_repos

    repos = get_session_repos()
    activity_repo = repos["activity"]
    plan_repo = repos["plan"]
    user_repo = repos["user"]

    try:
        body = validate_get_post_body(event, [
            "activity_id",
        ])
        check_user_signin(event)

        jwt_payload = extract_jwt(get_jwt_token(event))

        curr_user = user_repo.find_one_by_email(jwt_payload["email"])
        if not curr_user:
            raise ResourceNotFoundException

        activity_id = ObjectId(body["activity_id"])
        activity = activity_repo.find_one_by_id(activity_id)
        if not activity:
            raise ResourceNotFoundException

        plan_id = activity["plan_id"]
        plan = plan_repo.find_one_by_id(plan_id)
        if not plan:
            raise ResourceNotFoundException

        # only members can modify plan
        if curr_user["_id"] not in plan["members"]:
            raise ForbiddenException


        activity_repo.delete_one_by_id(activity_id)
        plan_repo.update_one_by_id(
            plan_id,
            {
                "$pull": {
                    "activities": activity_id
                }
            }
        )

        return handle_response({
            "code": HTTPStatus.NO_CONTENT.value,
            "body": ""
        })
    except HttpException as e:
        return handle_response(e.args[0])
