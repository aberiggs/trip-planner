"""Module providing the handler for create plan endpoint"""

import json
from planner.util.get_secret import get_secret


def lambda_handler(event, context):
    """Lambda handler that stores a plan to the database"""

    mongo_db_user = get_secret("mongo-db-connection-secret", "mongo_db_user")
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": mongo_db_user,
            }
        ),
    }
