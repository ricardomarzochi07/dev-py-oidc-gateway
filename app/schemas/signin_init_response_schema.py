from pydantic import BaseModel

from app.dto.authorize_url_dto import AuthorizeUrlDto


class SigninInitResponseSchema(BaseModel):
    prelogin_id: str
    authorize_url: str
