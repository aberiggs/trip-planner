"""Module providing function to validate plan's date"""

from datetime import datetime
from http import HTTPStatus
from planner.http.exception import HttpException


def get_plan_date(date: str):
    """Function that validates"""
    try:
        return datetime.strptime(date, "%m/%d/%y")
    except Exception as e:
        raise HttpException(
            {
                "code": HTTPStatus.BAD_REQUEST,
                "body": {
                    "message": "plan date should follow the format: %m/%d/%y"
                },
            }
        ) from e
