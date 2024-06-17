import json
from util.get_secret import get_secret
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

mongo_db_connect_url = get_secret("mongo_db_connect_url")
client = MongoClient(mongo_db_connect_url, server_api=ServerApi("1"))

def lambda_handler(event, context):
    try:
        # insert a test event document to MongoDB, Todo: error handling
        insert_result = client["tripPlanner"]["testEvents"].insert_one(json.loads(event["body"]))

        return {
            "statusCode": 201,
            "body": json.dumps({
                "inserted_id": str(insert_result.inserted_id),
            }),
        }
    
    except Exception as e:
        return {
            "statusCode": 503,
            "body": json.dumps({
                "message": str(e),
            }),
        }
    