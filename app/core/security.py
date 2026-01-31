import time
import hmac
import hashlib
from urllib.parse import parse_qsl
from jose import jwt

class TelegramInitDataError(Exception):
    pass

def verify_telegram_init_data(
    init_data: str,
    bot_token: str,
    max_age: int | None = None,
    max_age_seconds: int = 86400,
):
    data = dict(parse_qsl(init_data))
    if "hash" not in data:
        raise TelegramInitDataError("hash missing")

    if max_age is None:
        max_age = max_age_seconds

    auth_date = int(data.get("auth_date", 0))
    if time.time() - auth_date > max_age:
        raise TelegramInitDataError("initData expired")

    check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(data.items()) if k != "hash"
    )

    secret = hmac.new(
        b"WebAppData",
        bot_token.encode(),
        hashlib.sha256
    ).digest()

    calc_hash = hmac.new(
        secret,
        check_string.encode(),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(calc_hash, data["hash"]):
        raise TelegramInitDataError("invalid hash")

    return data

def create_jwt(tg_user_id: int, secret: str):
    return jwt.encode(
        {
            "sub": str(tg_user_id),
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600
        },
        secret,
        algorithm="HS256"
    )
