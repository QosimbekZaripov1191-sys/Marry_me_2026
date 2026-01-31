import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, ConfigDict

from app.core.config import settings
from app.core.security import verify_telegram_init_data, TelegramInitDataError
from app.core.jwt_utils import create_jwt

router = APIRouter(prefix="/auth", tags=["auth"])

class TelegramAuthIn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    init_data: str = Field(alias="initData")

@router.post("/telegram")
def telegram_auth(body: TelegramAuthIn):
    try:
        data = verify_telegram_init_data(
            init_data=body.init_data,
            bot_token=settings.telegram_bot_token,
            max_age_seconds=86400,
        )
    except TelegramInitDataError as e:
        raise HTTPException(status_code=401, detail=str(e))

    try:
        user = json.loads(data.get("user", "{}"))
        tg_user_id = int(user["id"])
    except Exception:
        raise HTTPException(status_code=400, detail="initData.user invalid")

    token = create_jwt({"sub": str(tg_user_id)})

    return {"access_token": token, "token_type": "bearer"}