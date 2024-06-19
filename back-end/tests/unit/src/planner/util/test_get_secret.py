from unittest import TestCase
from unittest.mock import patch
from moto import mock_aws
from src.planner.util.get_secret import get_secret
import boto3
from botocore.exceptions import ClientError
import pytest
import json

@mock_aws
class TestValidator(TestCase):
    def setUp(self) -> None:
        self.secret_name = "secret_name"
        self.secret_key = "secret_key"
        self.secret_value = "secret_value"
        self.region_name = "us-east-1"

        self.client = boto3.client("secretsmanager", region_name=self.region_name)
        secret_dict = {self.secret_key: self.secret_value}
        self.client.create_secret(Name=self.secret_name, SecretString=json.dumps(secret_dict))

    def test_get_secret_secret_exist(self):
        assert get_secret(self.secret_name, self.secret_key) == self.secret_value
    
    def test_get_secret_name_not_exit(self):
        with pytest.raises(ClientError):
            get_secret("fake name", self.secret_key)
    
    def test_get_secret_key_not_exist(self):
        with pytest.raises(ValueError):
            get_secret(self.secret_name, "fake key")


    def tearDown(self) -> None:
        pass