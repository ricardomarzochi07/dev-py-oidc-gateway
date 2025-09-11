from fastapi import Response
from pydantic import BaseModel


class CookieDto(BaseModel):
    key: str
    value: str
    httponly: bool
    samesite: str
    secure: bool
    max_age: int