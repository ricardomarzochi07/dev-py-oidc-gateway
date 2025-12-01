from pydantic import BaseModel
from datetime import time


class SigninPreLoginModel(BaseModel):
    state: str
    nonce: str
    code_verifier: str
    redirect_uri: str
    scope: str
    client_hint: str
    locale: str
    created_at: time
