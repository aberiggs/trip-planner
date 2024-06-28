"""Module providing unit tests for get_secret"""

import json
from unittest import TestCase
from moto import mock_aws
from planner.util.get_secret import get_secret
import boto3
from botocore.exceptions import ClientError
import pytest


@mock_aws
class TestValidator(TestCase):
    """Class containing all unit tests for get_secret"""

    def setUp(self) -> None:
        """Setup function that mocks the AWS Secrets Manager resource"""

        self.secret_name = "secret_name"
        self.secret_key = "secret_key"
        self.secret_value = "secret_value"
        self.region_name = "us-east-1"

        self.client = boto3.client(
            "secretsmanager", region_name=self.region_name
        )
        secret_dict = {self.secret_key: self.secret_value}
        self.client.create_secret(
            Name=self.secret_name, SecretString=json.dumps(secret_dict)
        )

    def test_get_secret_secret_exist(self):
        """Function that tests whether get_secret returns the correct secret value"""

        assert (
            get_secret(self.secret_name, self.secret_key) == self.secret_value
        )

    def test_get_secret_name_not_exit(self):
        """Function that tests whether get_secret raise an error when the secret
        name doesn't exist in AWS"""

        with pytest.raises(ClientError):
            get_secret("fake name", self.secret_key)

    def test_get_secret_key_not_exist(self):
        """Function that tests whether get_secret raise an error when the secret
        key doesn't exist in AWS"""

        with pytest.raises(ValueError):
            get_secret(self.secret_name, "fake key")

    def tearDown(self) -> None:
        pass
