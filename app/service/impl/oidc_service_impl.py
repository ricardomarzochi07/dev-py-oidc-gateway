from jose import JOSEError
import jwt
from app.clients.idp_service_client.wso2is_client import Wso2isClient
from buddybet_transactionmanager.http.transaction_http import HttpResponseSchema

from app.clients.idp_service_client.wso2is_paths import IdpPaths
from app.clients.signupcore_service_service.signup_core_service_client import SignupCoreServiceClient
from app.dto.authorize_url_dto import AuthorizeUrlDto
from app.dto.jwt_dto import JwtTokenDTO
from app.model.signin_prelogin_model import SigninPreLoginModel
from app.schemas.signin_init_request_schema import SigninInitRequestSchema
from app.schemas.signin_init_response_schema import SigninInitResponseSchema
from app.schemas.signupsubmit_request_schema import SignupSubmitRequest
from app.core.environment_config import AppConfig
from buddybet_logmon_common.logger import get_logger
import uuid
from jose import jwt
import json
from app.core.oidc_constants import Constants
from app.schemas.token_idp_schema import TokenIdpSchema
from app.schemas.token_internal_schema import TokenInternalSchema
from app.service.oidc_service import OidcTokenService
from app.utils.generate_codes_helper import generate_codes_signin
from app.utils.validate_code_helper import validate_token_internal
from app.core.exceptions import InvalidToken, JwtSigningError
from app.core.cache.base import Cache
from datetime import datetime
from app.core.i18n_instance import i18n


class OidcServiceImpl(OidcTokenService):
    logger = get_logger()

    def __init__(self, config: AppConfig, cache: Cache):
        self.cache = cache
        self.env_var = config.oidc_gateway_env

    async def orchestrate_signup_user(self, data: SignupSubmitRequest) -> HttpResponseSchema:
        self.logger.info("Execute orchestrate_signup_user")
        signup_service = SignupCoreServiceClient()
        wso2Client = Wso2isClient()

        # (1) - VALIDATE INTERNAL TOKEN JWT
        if validate_token_internal(internal_token=data.jwt_nonce, public_key=self.env_var.public_key):
            # (2) - INVOKE WSO2-IS
            idp_token = await wso2Client.get_access_token_for_signup(
                base_url=self.env_var.idp_service_url,
                client_id=self.env_var.oidc_client_id,
                client_secret=self.env_var.oidc_client_secret)
            # (4) - INVOKE SIGNUP REGISTER
            return await signup_service.register_in_signup_core(
                url_base=self.env_var.signup_core_service_url,
                data=data, access_token=idp_token.access_token)
        else:
            self.logger.error(f"Token inválido:", exc_info=True)
            raise InvalidToken()

    async def generate_idp_token(self, internal_token: str) -> TokenIdpSchema:
        self.logger.info("Execute Request - issue_wso2_token")
        wso2Client = Wso2isClient()
        if validate_token_internal(internal_token):
            token_idp_resp = await wso2Client.get_access_token_for_signup(
                base_url=self.env_var.idp_service_url,
                client_id=self.env_var.oidc_client_id,
                client_secret=self.env_var.oidc_client_secret
            )
        return token_idp_resp

    def generate_token_internal(self) -> JwtTokenDTO:
        self.logger.info("Execute generate_token_internal internal short - term")
        try:
            now = datetime.now().time()
            jwtToken = JwtTokenDTO(
                iss=Constants.ISSUER,
                sub=self.env_var.oidc_client_id,
                aud=Constants.AUDIENCE,
                iat=int(now),
                exp=int(now + self.env_var.time_exp_token),
                jti=str(uuid.uuid4()),
                scope=Constants.SCOPE_INTERNAL
            )
            token = jwt.encode(jwtToken.dict(), self.env_var.private_key, algorithm=Constants.ALGORITHM,
                               headers={"kid": self.env_var.kid_name})
            return TokenInternalSchema(
                jwt_nonce=token,
                token_type=Constants.TOKEN_TYPE,
                expires_in=self.env_var.time_exp_token
            )
        except JOSEError as e:
            self.logger.error(f"Error al firmar JWT: {str(e)}", exc_info=True)
            raise JwtSigningError()
