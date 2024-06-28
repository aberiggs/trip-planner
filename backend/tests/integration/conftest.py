"""Module providing mongodb client and session fixtures for integration tests"""

import pytest
import pymongo
from planner.util.get_secret import get_secret
from planner.db.user_schema import enforce_user_schema
from planner.db.create_collection import create_collection

@pytest.fixture(scope="session")
def client():
    """Function providing fixture to connect to MongoDB"""

    mongo_db_connect_url = get_secret(
        "mongo-db-connection-secret", "mongo_db_connect_url"
    )
    client = pymongo.MongoClient(mongo_db_connect_url)

    create_collection(client.trip_planner, "users")
    enforce_user_schema(client.trip_planner)

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
