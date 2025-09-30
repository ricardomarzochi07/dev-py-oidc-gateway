from buddybet_logmon_common.logger import get_logger

from app.clients.idp_service_client.wso2is_paths import IdpPaths
from app.core.exceptions import ConnectionFailIdp
from app.core.oidc_constants import Constants
import requests, time
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout
from app.schemas.token_idp_schema import TokenIdpSchema


class Wso2isClient:
    logger = get_logger()

    # Diccionario cache token WSO2
    cache = {"token": None, "exp": 0}


    async def get_access_token_for_signup(self, base_url: str, client_id: str, client_secret: str) -> TokenIdpSchema:
        self.logger.info("Execute Request - get_access_token_for_signup")
        now = int(time.time())
        expected_scope = Constants.SCOPE_SIGNUP_IDP
        url = base_url + IdpPaths.AUTH_TOKEN
        # Check cache for Token Valid
        if self.cache.get("access_token") and self.cache.get("expires_in") > now + 60:
            return TokenIdpSchema(
                access_token=self.cache["access_token"],
                token_type=self.cache["type"],
                expires_in=self.cache["expires_in"]
            )
        # Call WSO2 for get new Token
        try:
            response = requests.post(
                url,
                data={
                    "grant_type": "client_credentials",
                    "scope": expected_scope
                },
                auth=(client_id, client_secret),
                timeout=5,
                verify=False
            )
            response.raise_for_status()
            # Save new Token in Cache
            data = response.json()
            self.cache["access_token"] = data["access_token"]
            self.cache["type"] = Constants.TOKEN_TYPE
            self.cache["expires_in"] = now + data.get("expires_in", 1800)  # fallback 30 min

            return TokenIdpSchema(
                access_token=self.cache["access_token"],
                token_type=self.cache["type"],
                expires_in=self.cache["expires_in"]
            )

        except (HTTPError, ConnectionError, Timeout) as e:
            self.logger.error(f"WSO2 request failed: {str(e)}", exc_info=True)
            raise ConnectionFailIdp()
        except RequestException as e:
            self.logger.error(f"WSO2 unknown request error: {str(e)}", exc_info=True)
            raise ConnectionFailIdp()
        except ConnectionFailIdp as e:
            self.logger.error("WSO2 request failed", exc_info=True)
            raise ConnectionFailIdp()


