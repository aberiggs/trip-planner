"""Module providing the handler for activity creation"""

import json
from datetime import datetime
from http import HTTPStatus
from planner.db.activity_schema import enforce_activity_schema
from planner.http.validator import post_body_validator
from planner.http.response import response_handler
from planner.http.error import INVALID_BODY
from planner.db.create_collection import create_collection
from planner.db.db_init import db_init

def db_setup():
    """Function that sets up mongodb client, session, schema enforcement"""
    client, session = db_init()
    db = client.trip_planner
    create_collection(db, "activities")
    enforce_activity_schema(db)
    return db, session

def lambda_handler(event, context):
    """Lambda handler that creates an activity document in MongoDB"""
    try:
        body = json.loads(event["body"])
    except json.JSONDecodeError:
        return INVALID_BODY

    body_validator_response = post_body_validator(
        event, ["name", "location", "start_time", "end_time", "note"]
    )

    if body_validator_response is not None:
        return body_validator_response

    activity = {
        "name": body["name"],
        "location": body["location"],
        "start_time": datetime.strptime(body["start_time"], "%m/%d/%y %H:%M:%S"),
        "end_time": datetime.strptime(body["end_time"], "%m/%d/%y %H:%M:%S"),
        "note": body["note"]
    }

    db, session = db_setup()

    insert_result = db["activities"].insert_one(activity, session=session)

    print(str(insert_result.inserted_id))

    return response_handler(HTTPStatus.OK, {"inserted_id": str(insert_result.inserted_id)})
