import os
import time
from jose import jwt

def create_jwt(payload: dict) -> str:
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET is not set")

    p = payload.copy()
    p["exp"] = int(time.time()) + 60 * 60 * 24 * 7  # 7 дней

    return jwt.encode(p, secret, algorithm="HS256")