import jwt
from src.planner.util.get_secret import get_secret
from datetime import datetime, timezone

SECRET_KEY = get_secret("auth", "jwt_secret_key")

def jwt_validator(jwtToken):

    try:
        jwt.decode(jwtToken, key=SECRET_KEY, algorithms=["HS256"])
        header = jwt.get_unverified_header(jwtToken)

        if 'exp' not in header:
            return False
        
        exp = datetime.fromtimestamp(header['exp'], timezone.utc)
        now = datetime.now(timezone.utc)

        if now > exp:
            print('Token expired')
            return False
        
        return True
    except Exception:
        return False