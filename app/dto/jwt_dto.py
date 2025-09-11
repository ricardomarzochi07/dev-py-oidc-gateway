from pydantic import BaseModel


class JwtTokenDTO(BaseModel):
    iss: str
    sub: str
    aud: str
    iat: int
    exp: int
    jti: str
    scope: str
