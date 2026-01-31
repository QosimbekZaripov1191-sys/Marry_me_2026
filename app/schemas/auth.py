from pydantic import BaseModel, Field, ConfigDict

class TelegramAuthIn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    init_data: str = Field(alias="initData")

class AuthOut(BaseModel):
    access_token: str