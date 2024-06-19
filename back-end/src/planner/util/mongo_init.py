from get_secret import get_secret
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def mongo_init():
    mongo_db_connect_url = get_secret('mongo_db_connect_url')
    client = MongoClient(mongo_db_connect_url, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        return client
    except Exception as e:
        return e
