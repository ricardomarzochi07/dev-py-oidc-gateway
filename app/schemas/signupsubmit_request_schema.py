from pydantic import BaseModel


class SignupSubmitRequest(BaseModel):
    jwt_nonce: str
    jwt_csrf: str
    captcha_token: str
    firstName: str
    lastName: str
    gender: str
    email: str
    username: str
    password: str
