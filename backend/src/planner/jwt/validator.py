"""Module providing function to validate JWT token"""

from datetime import datetime, timezone
import jwt


def validate_jwt(jwt_token):
    """Function that validates JWT token with secret stored in AWS"""

    from planner.util.get_secret import get_secret

    secret_key = get_secret("auth", "jwt_secret_key")

    try:
        jwt.decode(jwt_token, key=secret_key, algorithms=["HS256"])
        header = jwt.get_unverified_header(jwt_token)

        if "exp" not in header:
            return False

        exp = datetime.fromtimestamp(header["exp"], timezone.utc)
        now = datetime.now(timezone.utc)

        if now > exp:
            print("[error] Token expired")
            return False

        return True
    except Exception:
        return False
