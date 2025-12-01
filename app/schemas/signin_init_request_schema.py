from pydantic import BaseModel

from app.dto.session_dto import SessionDTO


class SigninInitRequestSchema(BaseModel):
    redirect_uri: str
    scope: str
    locale: str
    client_hint: str
    session_context: SessionDTO
