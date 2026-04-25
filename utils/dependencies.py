from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import os

security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = int(payload.get("sub"))

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user_id

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")