from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class UploadIn(BaseModel):
    image_base64: str

@router.post("")
async def upload_base64(body: UploadIn):
    # MVP: возвращаем то же, что пришло
    return {"url": body.image_base64}