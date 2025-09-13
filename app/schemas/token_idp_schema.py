from pydantic import BaseModel


class TokenIdpSchema(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
