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
    ForbiddenException
)
from planner.http.response import handle_response
from planner.date.get_plan_date import get_plan_date
from planner.db.serialize.jsonify_plan import jsonify_plan

utc_now = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)

def lambda_handler(event, context):
    """Lambda handler that update a plan in the database"""
    from planner.db.repo.get_session_repos import get_session_repos

    repos = get_session_repos()
    user_repo = repos["user"]
    plan_repo = repos["plan"]

    try:
        body = validate_get_post_body(
            event, ["plan_id", "name", "date", "owner", "members", "activities"]
        )
        check_user_signin(event)

        jwt_payload = extract_jwt(get_jwt_token(event))

        curr_user = user_repo.find_one_by_email(jwt_payload["email"])
        if not curr_user:
            raise ResourceNotFoundException

        # only owner can modify owner field
        found_plan = plan_repo.find_one_by_id(ObjectId(body["plan_id"]))
        if (ObjectId(body["owner"]) != found_plan["owner"] and
                found_plan["owner"] != curr_user["_id"]):
            raise ForbiddenException

        # only members can modify plan
        if curr_user["_id"] not in found_plan["members"]:
            raise ForbiddenException

        # check if all members exist in the database
        members_id = []
        for member in body["members"]:
            member_id = ObjectId(member)
            if not user_repo.find_one_by_id(member_id):
                raise ResourceNotFoundException
            members_id.append(member_id)

        plan = {
            "_id": ObjectId(body["plan_id"]),
            "name": body["name"],
            "date": get_plan_date(body["date"]),
            "owner": curr_user["_id"],
            "members": members_id,
            "activities": body["activities"]
        }

        plan_repo.update_one_by_id(
            ObjectId(body["plan_id"]),
            {
                "$set": {
                    "name": body["name"],
                    "date": get_plan_date(body["date"]),
                    "members": members_id,
                },
            },
        )

        return handle_response(
            {"code": HTTPStatus.CREATED.value, "body": jsonify_plan(plan)}
        )

    except HttpException as e:
        return handle_response(e.args[0])
