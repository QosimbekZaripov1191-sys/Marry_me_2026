import hashlib
import hmac
import json
import time
from urllib.parse import parse_qsl

from fastapi import HTTPException

from app.core.config import settings


def verify_init_data(init_data: str, max_age_seconds: int = 86400) -> dict:
    """
    Строгая проверка Telegram WebApp initData:
    - hash сравниваем через HMAC-SHA256
    - secret_key = sha256(bot_token)
    - проверяем auth_date (не старше max_age_seconds)
    Возвращаем dict со всеми полями + распарсенный user (dict).
    """
    if not init_data or not init_data.strip():
        raise HTTPException(status_code=400, detail="initData is empty")

    pairs = list(parse_qsl(init_data, keep_blank_values=True))

    data = dict(pairs)
    recv_hash = data.get("hash")
    if not recv_hash:
        raise HTTPException(status_code=400, detail="initData: missing hash")

    # auth_date freshness
    auth_date_str = data.get("auth_date")
    if not auth_date_str:
        raise HTTPException(status_code=400, detail="initData: missing auth_date")
    try:
        auth_date = int(auth_date_str)
    except Exception:
        raise HTTPException(status_code=400, detail="initData: invalid auth_date")

    now = int(time.time())
    if now - auth_date > max_age_seconds:
        raise HTTPException(status_code=401, detail="initData expired")

    # build data_check_string (exclude hash)
    check_items = []
    for k, v in sorted(pairs, key=lambda x: x[0]):
        if k == "hash":
            continue
        check_items.append(f"{k}={v}")
    data_check_string = "\n".join(check_items)

    bot_token = getattr(settings, "bot_token", None) or getattr(settings, "BOT_TOKEN", None)
    if not bot_token:
        raise HTTPException(status_code=500, detail="BOT_TOKEN is not set in settings")

    secret_key = hashlib.sha256(bot_token.encode("utf-8")).digest()
    calc_hash = hmac.new(secret_key, data_check_string.encode("utf-8"), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(calc_hash, recv_hash):
        raise HTTPException(status_code=401, detail="initData signature invalid")

    # parse user json
    raw_user = data.get("user")
    if not raw_user:
        raise HTTPException(status_code=400, detail="initData: missing user")

    try:
        user_obj = json.loads(raw_user)
    except Exception:
        raise HTTPException(status_code=400, detail="initData: invalid user json")

    data["user"] = user_obj
    return data