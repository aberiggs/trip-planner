"""Module providing function to conect with MongoDB"""

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from planner.util.get_secret import get_secret


def db_init():
    """Function that connects to MongoDB and starts session"""

    mongo_db_connect_url = get_secret(
        "mongo-db-connection-secret", "mongo_db_connect_url"
    )
    client = MongoClient(mongo_db_connect_url, server_api=ServerApi("1"))
    session = client.start_session()
    return client, session
