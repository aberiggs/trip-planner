"""Module providing function to retrieve secret from AWS"""

import json
import boto3

def get_secret(secret_name, secret_key):
    """Function that retrieves secret from AWS Secrets Manager"""

    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager", region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    get_secret_value_response = json.loads(
        get_secret_value_response["SecretString"]
    )

    if secret_key not in get_secret_value_response:
        raise ValueError(f"{secret_key} does not exist")

    return get_secret_value_response[secret_key]
