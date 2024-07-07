"""Module providing the handler for update plan endpoint"""

import datetime
from http import HTTPStatus
from bson.objectid import ObjectId
from planner.middleware.check_user_signin import check_user_signin
from planner.jwt.extractor import extract_jwt
from planner.jwt.get_jwt_token import get_jwt_token
from planner.http.exception import HttpException, ResourceNotFoundException, ForbiddenException
from planner.http.response import handle_response
from planner.db.serialize.jsonify_plan import jsonify_expanded_plan
from planner.http.validator import validate_get_path_params

utc_now = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)

def expand_plan(plan, user_repo, activity_repo):
    """Function that expands plan to include details about owner, members, and activities"""

    owner = user_repo.find_one_by_id(plan["owner"])
    plan["owner"] = {
        "first_name": owner["first_name"],
        "last_name": owner["last_name"],
        "email": owner["email"],
        "picture": owner["picture"]
    }

    members_id = plan["members"]
    plan["members"] = []
    for member_id in members_id:
        member = user_repo.find_one_by_id(member_id)
        plan["members"].append({
            "first_name": member["first_name"],
            "last_name": member["last_name"],
            "email": member["email"],
            "picture": member["picture"]
        })

    activities_id = plan["activities"]
    plan["activities"] = []
    for activity_id in activities_id:
        activity = activity_repo.find_one_by_id(activity_id)
        plan["activities"].append({
            "activity_id": activity["_id"],
            "name": activity["name"],
            "location": activity["location"],
            "start_time": activity["start_time"],
            "end_time": activity["end_time"],
            "note": activity["note"],
        })
    return plan

def lambda_handler(event, context):
    """Lambda handler that update a plan in the database"""
    from planner.db.repo.get_session_repos import get_session_repos

    repos = get_session_repos()
    user_repo = repos["user"]
    plan_repo = repos["plan"]
    activity_repo = repos["activity"]

    try:
        check_user_signin(event)

        jwt_payload = extract_jwt(get_jwt_token(event))

        curr_user = user_repo.find_one_by_email(jwt_payload["email"])
        if not curr_user:
            raise ResourceNotFoundException

        params = validate_get_path_params(event, ["plan_id"])
        plan_id = ObjectId(params["plan_id"])

        if plan_id not in curr_user["plans"]:
            raise ForbiddenException

        plan = plan_repo.find_one_by_id(plan_id)
        plan = expand_plan(plan, user_repo, activity_repo)

        return handle_response({"code": HTTPStatus.OK.value, "body": jsonify_expanded_plan(plan)})

    except HttpException as e:
        return handle_response(e.args[0])
