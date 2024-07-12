"""Module providing function to create JWT token"""

import time
import jwt


def create_jwt_token(payload, expiration_time=None):
    """Function that creates JWT token with secret stored in AWS"""
    from planner.util.get_secret import get_secret

    secret_key = get_secret("auth", "jwt_secret_key")

    if expiration_time is None:
        current_time = int(time.time())
        expiration_time = current_time + 864000  # ten days

    token = jwt.encode(
        payload, secret_key, algorithm="HS256", headers={"exp": expiration_time}
    )

    return token
