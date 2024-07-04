"""Module providing the handler for create plan endpoint"""

import json
from planner.http.validator import post_body_validator
from planner.db.db_init import db_init
from planner.middleware.check_user_signin import check_user_signin
from planner.jwt.extractor import jwt_extractor
from planner.jwt.get_jwt_token import get_jwt_token
from planner.http.exception import HttpException, ResourceNotFoundException
from planner.http.response import response_handler
from planner.date.get_plan_date import get_plan_date
from planner.db.repo.user_repo import UserRepo
from planner.db.repo.plan_repo import PlanRepo


def db_setup():
    """Function thaht sets up mongodb client, session, schema enforcement"""
    client, session = db_init()
    db = client.trip_planner
    user_repo = UserRepo(db, session)
    plan_repo = PlanRepo(db, session)
    return user_repo, plan_repo


def lambda_handler(event, context):
    """Lambda handler that stores a plan to the database"""

    user_repo, plan_repo = db_setup()

    try:
        body = json.loads(event["body"])

        post_body_validator(event, ["name", "date", "owner"])
        check_user_signin(event)

        jwt_payload = jwt_extractor(get_jwt_token(event))

        if not user_repo.find_one_by_email(jwt_payload["email"]):
            raise ResourceNotFoundException

        plan = {
            "name": body["name"],
            "date": get_plan_date(body["date"]),
            "owner": jwt_payload["email"],
        }
        plan_repo.insert_one(plan)

        return {
            "statusCode": 201,
            "body": json.dumps(plan, sort_keys=True, default=str),
        }

    except HttpException as e:
        return response_handler(e.args[0])
