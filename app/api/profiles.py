from fastapi import APIRouter, Depends

from app.api.deps import get_current_user_id

router = APIRouter(tags=["profiles"])


@router.get("/me")
async def me(user_id: str = Depends(get_current_user_id)):
    return {"ok": True, "tg_user_id": user_id}
