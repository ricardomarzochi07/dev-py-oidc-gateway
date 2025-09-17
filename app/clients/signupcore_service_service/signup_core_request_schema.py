from pydantic import BaseModel


class SignupCoreRequest(BaseModel):
    firstName: str
    lastName: str
    gender: str
    email: str
    username: str
    password: str
