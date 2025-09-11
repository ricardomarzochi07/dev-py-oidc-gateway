from pydantic import BaseModel


class SignupInitDTO(BaseModel):
    jwt_nonce: str
    jwt_csrf: str
    captcha_token: str
