import json
from util.get_secret import get_secret

def lambda_handler(event, context):
    mongo_db_user = get_secret("mongo-db-connection-secret", "mongo_db_user")
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": mongo_db_user,
        }),
    }