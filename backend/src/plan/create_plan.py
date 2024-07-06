"""Module providing the handler for create plan endpoint"""

import datetime
from http import HTTPStatus
from planner.http.validator import validate_get_post_body
from planner.middleware.check_user_signin import check_user_signin
from planner.jwt.extractor import extract_jwt
from planner.jwt.get_jwt_token import get_jwt_token
from planner.http.exception import (
    HttpException,
    ResourceNotFoundException,
)
from planner.http.response import handle_response
from planner.date.get_plan_date import get_plan_date
from planner.db.serialize.jsonify_plan import jsonify_plan

utc_now = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)

def lambda_handler(event, context):
    """Lambda handler that stores a plan to the database"""
    from planner.db.repo.get_session_repos import get_session_repos

    repos = get_session_repos()
    user_repo = repos["user"]
    plan_repo = repos["plan"]

    try:
        body = validate_get_post_body(event, ["name", "date"])
        check_user_signin(event)

        jwt_payload = extract_jwt(get_jwt_token(event))

        curr_user = user_repo.find_one_by_email(jwt_payload["email"])
        if not curr_user:
            raise ResourceNotFoundException

        plan = {
            "name": body["name"],
            "date": get_plan_date(body["date"]),
            "owner": curr_user["_id"],
            "members": [curr_user["_id"]],
        }
        plan_repo.insert_one(plan)
        user_repo.update_one_by_email(
            curr_user["email"],
            {
                "$set": {
                    "last_visited": utc_now,
                },
                "$push": {"plans": plan["_id"]},
            },
        )

        jsonify_plan(plan)

        return handle_response({"code": HTTPStatus.CREATED.value, "body": plan})

    except HttpException as e:
        return handle_response(e.args[0])
