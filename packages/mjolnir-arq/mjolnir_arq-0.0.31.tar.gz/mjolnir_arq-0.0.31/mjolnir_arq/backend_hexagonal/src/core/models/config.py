from typing import Any, Optional
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from src.core.enums.response_type import RESPONSE_TYPE
from src.core.models.access_token import AccessToken


class Config(BaseModel):
    db: Optional[Any] = None
    language: Optional[str] = None
    request: Optional[Any] = None
    response_type: RESPONSE_TYPE = Field(default=RESPONSE_TYPE.DICT.value)
    token: Optional[AccessToken] = Field(default=None)
    token_code: Optional[str] = Field(default=None)
