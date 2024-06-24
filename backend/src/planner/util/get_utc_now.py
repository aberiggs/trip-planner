"""Module providing function to retrieve the current UTC time"""

import datetime


def get_utc_now():
    """Function that returns the current UTC time"""

    return datetime.datetime.now(tz=datetime.timezone.utc).replace(
        microsecond=0
    )
