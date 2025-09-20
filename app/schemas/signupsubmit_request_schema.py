from pydantic import BaseModel, ConfigDict


class SignupSubmitRequest(BaseModel):
    jwt_nonce: str
    firstName: str
    lastName: str
    gender: str
    email: str
    username: str
    password: str

    model_config = ConfigDict(extra="ignore")
