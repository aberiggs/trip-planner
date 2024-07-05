"""Module providing the handler for create plan endpoint"""

import json
import datetime
from http import HTTPStatus
from planner.http.validator import post_body_validator
from planner.db.db_init import db_init
from planner.middleware.check_user_signin import check_user_signin
from planner.jwt.extractor import jwt_extractor
from planner.jwt.get_jwt_token import get_jwt_token
from planner.http.exception import HttpException, ResourceNotFoundException, InvalidBodyException
from planner.http.response import response_handler
from planner.date.get_plan_date import get_plan_date
from planner.db.repo.user_repo import UserRepo
from planner.db.repo.plan_repo import PlanRepo

utc_now = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0)

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
        try:
            body = json.loads(event["body"])
        except json.JSONDecodeError as e:
            raise InvalidBodyException from e

        post_body_validator(event, ["name", "date", "owner"])
        check_user_signin(event)

        jwt_payload = jwt_extractor(get_jwt_token(event))

        curr_user = user_repo.find_one_by_email(jwt_payload["email"])
        if not curr_user:
            raise ResourceNotFoundException

        plan = {
            "name": body["name"],
            "date": get_plan_date(body["date"]),
            "owner": curr_user["_id"],
            "members": []
        }
        plan_repo.insert_one(plan)
        user_repo.update_one(
            curr_user["email"],
            {
                "$set": {
                    "last_visited": utc_now,
                },
                "$push": {
                    "plans": plan["_id"]
                }
            },
        )

        plan["date"] = plan["date"].strftime("%m/%d/%y")
        plan["owner"] = str(plan["owner"])
        plan["_id"] = str(plan["_id"])

        return response_handler({
            "code": HTTPStatus.CREATED.value,
            "body": plan
        })

    except HttpException as e:
        return response_handler(e.args[0])
