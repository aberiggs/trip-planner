"""Module providing function to extract and validate plan's date"""

from datetime import datetime
from http import HTTPStatus
from planner.http.exception import HttpException


def get_plan_date(date: str):
    """Function that convert date string to datetime object while validating the
    date format"""
    try:
        return datetime.strptime(date, "%m/%d/%y")
    except Exception as e:
        raise HttpException(
            {
                "code": HTTPStatus.BAD_REQUEST.value,
                "body": {
                    "message": "plan date should follow the format: %m/%d/%y"
                },
            }
        ) from e
