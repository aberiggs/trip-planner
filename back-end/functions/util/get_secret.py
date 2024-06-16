import boto3
from botocore.exceptions import ClientError
import json

def get_secret(secret_name, secret_key):
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        get_secret_value_response = json.loads(get_secret_value_response['SecretString'])
    except ClientError as e:
        raise e
    
    if secret_key not in get_secret_value_response:
        return "secret_key doesn't exist"

    return get_secret_value_response[secret_key]