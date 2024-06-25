"""Module providing the handler for activity creation"""

import json
from planner.util.get_secret import get_secret
from planner.db.activities_schema import enforce_activities_schema
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

mongo_db_connect_url = get_secret(
    "mongo-db-connection-secret", "mongo_db_connect_url"
)
client = MongoClient(mongo_db_connect_url, server_api=ServerApi("1"))

db = client.trip_planner
enforce_activities_schema(db)


def lambda_handler(event, context):
    """Lambda handler that creates an activity document in MongoDB"""
    try:
        # insert a test activity document to MongoDB, Todo: error handling
        insert_result = client["trip_planner"]["activities"].insert_one(
            json.loads(event["body"])
        )

        print(str(insert_result.inserted_id))
        return {
            "statusCode": 201,
            "body": json.dumps(
                {
                    "inserted_id": str(insert_result.inserted_id),
                }
            ),
        }

    except Exception as e:
        print(str(e))
        return {
            "statusCode": 503,
            "body": json.dumps(
                {
                    "message": str(e),
                }
            ),
        }
