from app.clients.wso2is_client import Wso2isClient
from app.core.oidc_constants import IAMConstants
from app.dto.jwt_dto import JwtTokenDTO
from app.schemas.token_idp_schema import TokenIdpSchema
from app.schemas.token_internal_schema import TokenInternalSchema
from app.service.oidc_service import OidcService
from app.core.environment_config import AppConfig
from buddybet_logmon_common.logger import get_logger
import jwt
from jose import jwt, JWTError
import time, uuid
from fastapi import HTTPException


class OidcServiceImpl(OidcService):
    logger = get_logger()

    def __init__(self, config: AppConfig):
        self.env_var = config.oidc_gateway_env
        self.wso2Client = Wso2isClient(config)

    def validate_token_internal(self, internal_token: str):
        self.logger.info("Execute Request - validate_internal_token")
        try:
            # Validar JWT interno del broker
            self.logger.info("Validar Token Interno - issue_wso2_token")
            print(" self.env_var.public_key :::::::::::::: ",  self.env_var.public_key)
            jwt.decode(internal_token, self.env_var.public_key, algorithms=IAMConstants.ALGORITHM,
                       audience=IAMConstants.AUDIENCE)
        except JWTError as e:
            self.logger.error("Token inválido", exc_info=True)
            raise HTTPException(status_code=401, detail="Invalid token")

    def generate_idp_token(self, internal_token: str) -> TokenIdpSchema:
        self.logger.info("Execute Request - issue_wso2_token")
        try:
            self.validate_token_internal(internal_token)
            idp_token = self.wso2Client.get_token_in_client_credential()

            tokenSchemaResp = TokenIdpSchema(
                access_token=idp_token.token,
                token_type=IAMConstants.TOKEN_TYPE,
                expires_in=idp_token.exp
            )
            return tokenSchemaResp
        except Exception as e:
            self.logger.error("Error Execute Request - orchestrate_signup_init", exc_info=True)

    def generate_token_internal(self) -> TokenInternalSchema:
        self.logger.info("Execute generate_token_internal internal short - term")

        try:
            now = time.time()
            jwtToken = JwtTokenDTO(
                iss=IAMConstants.ISSUER,
                sub=self.env_var.oidc_client_id,
                aud=IAMConstants.AUDIENCE,
                iat=int(now),
                exp=int(now + self.env_var.time_exp_token),
                jti=str(uuid.uuid4()),
                scope=IAMConstants.SCOPE
            )
            token = jwt.encode(jwtToken.dict(), self.env_var.private_key, algorithm=IAMConstants.ALGORITHM,
                               headers={"kid": self.env_var.kid_name})
            tokenResp = TokenInternalSchema(
                jwt_nonce=token,
                token_type=IAMConstants.TOKEN_TYPE,
                expires_in=self.env_var.time_exp_token
            )
            return tokenResp
        except Exception as e:
            self.logger.error("Error Execute Request - generate_token", e)
