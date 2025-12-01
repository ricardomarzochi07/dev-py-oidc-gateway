from pydantic import BaseModel
from typing import Optional


class AppConfigEnvironment(BaseModel):
    redis_url: str
    cache_default_ttl: int
    idp_service_url: str
    oidc_client_id: str
    oidc_client_secret: str
    time_exp_token: int
    kid_name: str
    public_key: Optional[bytes] = None
    private_key: Optional[bytes] = None
    signup_core_service_url: str
    idp_audience_signup_register: str
    idp_scope_signup: str


class AppConfig(BaseModel):
    oidc_gateway_env: AppConfigEnvironment
