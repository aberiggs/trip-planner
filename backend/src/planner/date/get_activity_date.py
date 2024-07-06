"""Module providing function to extract and validate activities's date"""

from datetime import datetime
from http import HTTPStatus
from planner.http.exception import HttpException


def get_activity_date(date: str):
    """Function that convert date string to datetime object while validating the
    date format"""

    try:
        return datetime.strptime(date, "%m/%d/%y %H:%M:%S")
    except Exception as e:
        raise HttpException(
            {
                "code": HTTPStatus.BAD_REQUEST,
                "body": {
                    "message": "activity time should follow the format: %m/%d/%y %H:%M:%S"
                },
            }
        ) from e
