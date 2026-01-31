import time
from jose import jwt

from app.core.config import settings

def create_jwt(payload: dict) -> str:
    p = payload.copy()
    p["exp"] = int(time.time()) + 60 * 60 * 24 * 7  # 7 дней

    return jwt.encode(p, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
