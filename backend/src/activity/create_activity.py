"""Module providing the handler for activity creation"""

from http import HTTPStatus
from bson.objectid import ObjectId
from planner.http.validator import validate_get_post_body
from planner.middleware.check_user_signin import check_user_signin
from planner.http.response import handle_response
from planner.date.get_activity_date import get_activity_date
from planner.db.serialize.jsonify_activity import jsonify_activity
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
            "name",
            "location",
            "start_time",
            "end_time",
            "note",
            "plan_id"
        ])
        check_user_signin(event)

        jwt_payload = extract_jwt(get_jwt_token(event))

        curr_user = user_repo.find_one_by_email(jwt_payload["email"])
        if not curr_user:
            raise ResourceNotFoundException

        plan_id = ObjectId(body["plan_id"])
        plan = plan_repo.find_one_by_id(plan_id)
        if not plan:
            raise ResourceNotFoundException

        # only members can modify plan
        if curr_user["_id"] not in plan["members"]:
            raise ForbiddenException

        activity = {
            "name": body["name"],
            "location": body["location"],
            "start_time": get_activity_date(body["start_time"]),
            "end_time": get_activity_date(body["end_time"]),
            "note": body["note"],
            "plan_id": plan_id
        }

        activity_repo.insert_one(activity)
        plan_repo.update_one_by_id(
            plan_id,
            {
                "$push": {
                    "activities": activity["_id"]
                }
            }
        )

        return handle_response({
            "code": HTTPStatus.CREATED.value,
            "body": jsonify_activity(activity)
        })
    except HttpException as e:
        return handle_response(e.args[0])
