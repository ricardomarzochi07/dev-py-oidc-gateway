from pydantic import BaseModel


class AccessTokenWso2(BaseModel):
    token: str
    exp: int