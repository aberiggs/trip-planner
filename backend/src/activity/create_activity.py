"""Module providing the handler for activity creation"""

from http import HTTPStatus
from planner.http.validator import validate_get_post_body
from planner.middleware.check_user_signin import check_user_signin
from planner.http.response import handle_response
from planner.date.get_activity_date import get_activity_date
from planner.db.serialize.jsonify_activity import jsonify_activity
from planner.http.exception import (
    HttpException,
)

def lambda_handler(event, context):
    """Lambda handler that creates an activity document in MongoDB"""
    from planner.db.repo.get_session_repos import get_session_repos

    repos = get_session_repos()
    activity_repo = repos["activity"]

    try:
        body = validate_get_post_body(event, ["name", "location", "start_time", "end_time", "note"])
        check_user_signin(event)

        activity = {
            "name": body["name"],
            "location": body["location"],
            "start_time": get_activity_date(body["start_time"]),
            "end_time": get_activity_date(body["end_time"]),
            "note": body["note"]
        }

        activity_repo.insert_one(activity)

        return handle_response({
            "code": HTTPStatus.OK.value,
            "body": jsonify_activity(activity)
        })
    except HttpException as e:
        return handle_response(e.args[0])
