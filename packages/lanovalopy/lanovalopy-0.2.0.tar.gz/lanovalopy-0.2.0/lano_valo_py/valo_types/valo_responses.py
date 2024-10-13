from typing import Any, Dict, Optional
from pydantic import BaseModel


class RateLimit(BaseModel):
    used: int
    remaining: int
    reset: int


class ErrorObject(BaseModel):
    message: str


class APIResponseModel(BaseModel):
    status: int
    data: Optional[Dict[str, Any]] = None
    ratelimits: Optional[RateLimit] = None
    error: Optional[ErrorObject] = None
    url: Optional[str] = None