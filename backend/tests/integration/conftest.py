"""Module providing mongodb client and session fixtures for integration tests"""

from unittest.mock import patch
import pytest
import pymongo
from planner.util.get_secret import get_secret
from planner.db.repo.user_repo import UserRepo
from planner.db.repo.plan_repo import PlanRepo
from planner.db.repo.activity_repo import ActivityRepo

@pytest.fixture(scope="session")
def client():
    """Function providing fixture to connect to MongoDB"""

    mongo_db_connect_url = get_secret(
        "mongo-db-connection-secret", "mongo_db_connect_url"
    )
    client = pymongo.MongoClient(mongo_db_connect_url)

    assert (
        client.admin.command("ping")["ok"] != 0.0
    )  # check the connection is ok
    return client


@pytest.fixture()
def rollback_session(client):
    """Function providing fixture to roll back session at the end of each test function"""

    session = client.start_session()
    session.start_transaction()

    try:
        yield session
    finally:
        session.abort_transaction()


@pytest.fixture()
def user_repo(client, rollback_session):
    """Function providing fixture to use user repo"""

    return UserRepo(client.trip_planner, rollback_session)


@pytest.fixture()
def plan_repo(client, rollback_session):
    """Function providing fixture to use user repo"""

    return PlanRepo(client.trip_planner, rollback_session)


@pytest.fixture()
def activity_repo(client, rollback_session):
    """Function providing fixture to use user repo"""

    return ActivityRepo(client.trip_planner, rollback_session)


@pytest.fixture
def patch_get_session_repos(user_repo, plan_repo, activity_repo):
    """Function that provides fixture to patch get_session_repos so that transactions
    are properly rolled back at the end of the test"""

    with patch(
        "planner.db.repo.get_session_repos.get_session_repos",
        return_value={
            "user": user_repo,
            "plan": plan_repo,
            "activity": activity_repo
        },
        autospec=True,
    ) as m:
        yield m
