"""Module providing the handler for get plans endpoint"""

import datetime
from http import HTTPStatus
from planner.middleware.check_user_signin import check_user_signin
from planner.jwt.extractor import extract_jwt
from planner.jwt.get_jwt_token import get_jwt_token
from planner.http.exception import HttpException, ResourceNotFoundException
from planner.http.response import handle_response
from planner.db.serialize.jsonify_plan import jsonify_plan

utc_now = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)

def lambda_handler(event, context):
    """Lambda handler that get plans from the database"""
    from planner.db.repo.get_session_repos import get_session_repos

    repos = get_session_repos()
    user_repo = repos["user"]
    plan_repo = repos["plan"]

    try:
        check_user_signin(event)

        jwt_payload = extract_jwt(get_jwt_token(event))

        curr_user = user_repo.find_one_by_email(jwt_payload["email"])
        if not curr_user:
            raise ResourceNotFoundException

        plans = []
        for plan_id in curr_user["plans"]:
            found = plan_repo.find_one_by_id(plan_id)
            plans.append(jsonify_plan(found))

        return handle_response({"code": HTTPStatus.OK.value, "body": plans})

    except HttpException as e:
        return handle_response(e.args[0])
