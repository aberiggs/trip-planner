"""Module providing the handler for update plan endpoint"""

import datetime
from http import HTTPStatus
from bson.objectid import ObjectId
from planner.middleware.check_user_signin import check_user_signin
from planner.jwt.extractor import extract_jwt
from planner.jwt.get_jwt_token import get_jwt_token
from planner.http.exception import HttpException, ResourceNotFoundException, ForbiddenException
from planner.http.response import handle_response
from planner.db.serialize.jsonify_activity import jsonify_activity
from planner.http.validator import validate_get_path_params

utc_now = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)

def lambda_handler(event, context):
    """Lambda handler that gets an activity from the database"""
    from planner.db.repo.get_session_repos import get_session_repos

    repos = get_session_repos()
    user_repo = repos["user"]
    activity_repo = repos["activity"]

    try:
        check_user_signin(event)

        jwt_payload = extract_jwt(get_jwt_token(event))

        curr_user = user_repo.find_one_by_email(jwt_payload["email"])
        if not curr_user:
            raise ResourceNotFoundException

        params = validate_get_path_params(event, ["activity_id"])
        activity_id = ObjectId(params["activity_id"])

        activity = activity_repo.find_one_by_id(activity_id)
        if not activity:
            raise ResourceNotFoundException

        plan_id = activity["plan_id"]
        if plan_id not in curr_user["plans"]:
            raise ForbiddenException

        activity = activity_repo.find_one_by_id(activity_id)
        return handle_response({"code": HTTPStatus.OK.value, "body": jsonify_activity(activity)})

    except HttpException as e:
        return handle_response(e.args[0])
