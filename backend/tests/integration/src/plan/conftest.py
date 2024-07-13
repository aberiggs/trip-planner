"""Module providing common fixtures among plan integration tests"""

import datetime
import pytest
from planner.util.password import hash_password


@pytest.fixture()
def utc_now():
    """Function providing fixture to use utc_now"""

    return datetime.datetime.now(tz=datetime.timezone.utc).replace(
        microsecond=0
    )

@pytest.fixture()
def user(utc_now):
    """Function providing fixture to use user"""

    return {
        "first_name": "Steve",
        "last_name": "Bob",
        "picture": "steve.bob.png",
        "email": "steve.bob@email.com",
        "password": hash_password("steve's secure password"),
        "last_visited": utc_now.replace(tzinfo=None),
        "google_signup": False,
        "plans": [],
    }

@pytest.fixture()
def user2(utc_now):
    """Function providing fixture to use user2"""

    return {
        "first_name": "Cool",
        "last_name": "Bob",
        "picture": "cool.bob.png",
        "email": "cool.bob@email.com",
        "password": hash_password("cool's secure password"),
        "last_visited": utc_now.replace(tzinfo=None),
        "google_signup": False,
        "plans": [],
    }

@pytest.fixture()
def plan_info():
    """Function providing fixture to use plan_info"""

    return {
        "name": "steve's plan",
        "date": "09/19/22",
    }

@pytest.fixture()
def plan_info2(utc_now):
    """Function providing fixture to use plan_info2"""

    return {
        "name": "steve's second plan",
        "date": "09/20/22",
    }

@pytest.fixture()
def activity_info():
    """Function providing fixture to use activity_info"""

    return {
        "name": "eating at the dining court",
        "location": "dining court",
        "start_time": "09/19/22 13:55:26",
        "end_time": "09/19/22 15:35:12",
        "note": "eating with bob",
    }
