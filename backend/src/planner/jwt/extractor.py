"""Module providing function to extract info from JWT token"""

import jwt
from planner.util.get_secret import get_secret

SECRET_KEY = get_secret("auth", "jwt_secret_key")


def jwt_extractor(jwt_token):
    """Function that extracts info from JWT token. It DOES NOT validate the token."""

    info = jwt.decode(jwt_token, options={"verify_signature": False})
    return info
