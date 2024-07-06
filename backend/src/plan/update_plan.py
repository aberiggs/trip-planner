"""Module providing the handler for update plan endpoint"""

import datetime
from http import HTTPStatus
from bson.objectid import ObjectId
from planner.http.validator import validate_get_post_body
from planner.db.db_init import db_init
from planner.middleware.check_user_signin import check_user_signin
from planner.jwt.extractor import jwt_extractor
from planner.jwt.get_jwt_token import get_jwt_token
from planner.http.exception import (
    HttpException,
    ResourceNotFoundException,
)
from planner.http.response import response_handler
from planner.date.get_plan_date import get_plan_date
from planner.db.repo.user_repo import UserRepo
from planner.db.repo.plan_repo import PlanRepo
from planner.db.serialize.plan_serializer import plan_serializer

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
        body = validate_get_post_body(
            event, ["plan_id", "name", "date", "owner", "members"]
        )
        check_user_signin(event)

        jwt_payload = jwt_extractor(get_jwt_token(event))

        curr_user = user_repo.find_one_by_email(jwt_payload["email"])
        if not curr_user:
            raise ResourceNotFoundException

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

        return response_handler(
            {"code": HTTPStatus.CREATED.value, "body": plan_serializer(plan)}
        )

    except HttpException as e:
        return response_handler(e.args[0])
