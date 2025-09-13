from pydantic import BaseModel


class TokenInternalSchema(BaseModel):
    jwt_nonce: str
    token_type: str
    expires_in: int
