import json
from planner.jwt.validator import jwt_validator
from planner.http.validator import header_validator
from planner.http.response import response_handler

def lambda_handler(event, context):
    header_validator_response = header_validator(event, ['Authorization'])
    
    if header_validator_response is not None:
        return header_validator_response

    jwtToken = event['headers']['Authorization'].split(" ")[1].encode("utf-8")
    
    if jwt_validator(jwtToken):
        return response_handler(200, { "message": "you are logged in" })

    return response_handler(401, { "message": "you are not logged in" })