from buddybet_logmon_common.logger import get_logger
from app.core.environment_config import AppConfig
import requests, time
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import FastAPI, Depends, HTTPException

from app.dto.accesstoken_wso2_dto import AccessTokenWso2


class Wso2isClient:
    logger = get_logger()

    # Diccionario cache token WSO2
    cache = {"token": None, "exp": 0}

    def __init__(self, config: AppConfig):
        self.env_var = config.oidc_gateway_env

    def get_token_in_client_credential(self) -> AccessTokenWso2:
        self.logger.info("Execute Request - client_credential_token")
        now = int(time.time())
        # Check cache for Token Valid
        if self.cache.get("token") and self.cache.get("exp") > now + 60:
            return AccessTokenWso2(
                token=self.cache["token"],
                exp=self.cache["exp"]
            )
        # Call WSO2 for get new Token
        try:
            response = requests.post(
                self.env_var.wso2_token_url,
                data={"grant_type": "client_credentials"},
                auth=(self.env_var.oidc_client_id, self.env_var.oidc_client_secret),
                timeout=5,
                verify=False
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logger.error("WSO2 request failed", exc_info=True)
            raise HTTPException(status_code=502, detail="WSO2 token endpoint not reachable")

        # Save new Token in Cache
        data = response.json()
        self.cache["token"] = data["access_token"]
        self.cache["exp"] = now + data.get("expires_in", 1800) # fallback 30 min

        return AccessTokenWso2(
            token=self.cache["token"],
            exp=self.cache["exp"]
        )
