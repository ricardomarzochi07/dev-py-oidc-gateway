from pydantic import BaseModel
from typing import Optional


class AppConfigEnvironment(BaseModel):
    wso2_token_url: str
    oidc_client_id: str
    oidc_client_secret: str
    time_exp_token: int
    kid_name: str
    public_key: Optional[bytes] = None
    private_key: Optional[bytes] = None


class AppConfig(BaseModel):
    oidc_gateway_env: AppConfigEnvironment
