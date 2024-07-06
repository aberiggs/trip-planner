"""Module providing the handler for update plan endpoint"""

import datetime
from http import HTTPStatus
from planner.db.db_init import db_init
from planner.middleware.check_user_signin import check_user_signin
from planner.jwt.extractor import extract_jwt
from planner.jwt.get_jwt_token import get_jwt_token
from planner.http.exception import HttpException, ResourceNotFoundException
from planner.http.response import handle_response
from planner.db.repo.user_repo import UserRepo
from planner.db.repo.plan_repo import PlanRepo
from planner.db.serialize.jsonify_plan import jsonify_plan

utc_now = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)


def db_setup():
    """Function thaht sets up user and plan repos"""
    client, session = db_init()
    db = client.trip_planner
    user_repo = UserRepo(db, session)
    plan_repo = PlanRepo(db, session)
    return user_repo, plan_repo


def lambda_handler(event, context):
    """Lambda handler that update a plan in the database"""

    user_repo, plan_repo = db_setup()

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
