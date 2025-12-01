from pydantic import BaseModel


class OidcPkceDTO(BaseModel):
    state = str
    nonce = str
    code_verifier = str
    code_challenge = str
