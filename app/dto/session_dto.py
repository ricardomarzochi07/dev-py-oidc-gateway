from pydantic import BaseModel


class SessionDTO(BaseModel):
    jwt_nonce: str
    jwt_csrf: str
    captcha_token: str
