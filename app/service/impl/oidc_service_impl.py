from buddybet_idpsecure.authorization.transaction_auth import TransactionAuthorization
from buddybet_idpsecure.model.user_claims import UserClaims
from app.clients.idp_service_client.wso2is_client import Wso2isClient
from buddybet_transactionmanager.http.transaction_http import HttpResponseSchema
from app.clients.signupcore_service_service.signup_core_service_client import SignupCoreServiceClient
from app.core.oidc_constants import Constants
from app.dto.jwt_dto import JwtTokenDTO
from app.schemas.signupsubmit_request_schema import SignupSubmitRequest
from app.schemas.token_idp_schema import TokenIdpSchema
from app.schemas.token_internal_schema import TokenInternalSchema
from app.core.environment_config import AppConfig
from buddybet_logmon_common.logger import get_logger
import jwt
from jose import jwt, JWTError
import time, uuid
from fastapi import HTTPException
from app.service.oidc_service import OidcTokenService


class OidcServiceImpl(OidcTokenService):
    logger = get_logger()

    def __init__(self, config: AppConfig):
        self.env_var = config.oidc_gateway_env

    def validate_token_internal(self, internal_token: str):
        self.logger.info("Execute Request - validate_internal_token")
        try:
            # Validar JWT interno del broker
            #validate_token
            self.logger.info("Validar Token Interno - issue_wso2_token")
            print(" self.env_var.public_key :::::::::::::: ", self.env_var.public_key)
            jwt.decode(internal_token, self.env_var.public_key, algorithms=Constants.ALGORITHM,
                       audience=Constants.AUDIENCE)
        except JWTError as e:
            self.logger.error("Token inválido", exc_info=True)
            raise HTTPException(status_code=401, detail="Invalid token")

    async def validate_token_idp_for_signup(self, idp_token: str):
        self.logger.info("Execute Request - validate_token_idp")
        try:
            auth_token = TransactionAuthorization(idp_token)
            user_token: UserClaims = await auth_token.transaction_valid(None)

            expected_scope = self.env_var.idp_scope_signup
            if user_token.scope is not None:
                scopes = user_token.scope
                if expected_scope not in scopes:
                    self.logger.error("Token/Scope Inválido", exc_info=True)
                    raise HTTPException(status_code=401, detail="Token/Scope Invalid token scope not allowed")

        except JWTError as e:
            self.logger.error("Token inválido", exc_info=True)
            raise HTTPException(status_code=401, detail="Invalid token")

    async def generate_idp_token(self, internal_token: str) -> TokenIdpSchema:
        self.logger.info("Execute Request - issue_wso2_token")
        wso2Client = Wso2isClient()
        try:
            self.validate_token_internal(internal_token)
            idp_token = await wso2Client.get_access_token_for_signup(
                base_url=self.env_var.idp_service_url,
                client_id=self.env_var.oidc_client_id,
                client_secret=self.env_var.oidc_client_secret
            )
            return idp_token
        except Exception as e:
            self.logger.error("Error Execute Request - orchestrate_signup_init", exc_info=True)

    def generate_token_internal(self) -> TokenInternalSchema:
        self.logger.info("Execute generate_token_internal internal short - term")
        try:
            now = time.time()
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
            tokenResp = TokenInternalSchema(
                jwt_nonce=token,
                token_type=Constants.TOKEN_TYPE,
                expires_in=self.env_var.time_exp_token
            )
            return tokenResp
        except Exception as e:
            self.logger.error("Error Execute Request - generate_token", e)

    async def orchestrate_signup_user(self, data: SignupSubmitRequest) -> HttpResponseSchema:
        self.logger.info("Execute orchestrate_signup_user")
        signup_service = SignupCoreServiceClient()
        wso2Client = Wso2isClient()
        try:
            # (1) - VALIDATE INTERNAL TOKEN JWT
            self.validate_token_internal(data.jwt_nonce)
            # (2) - INVOKE WSO2-IS
            idp_token = await wso2Client.get_access_token_for_signup(
                base_url=self.env_var.idp_service_url,
                client_id=self.env_var.oidc_client_id,
                client_secret=self.env_var.oidc_client_secret
            )
            # (3) VALIDATE IDP TOKEN JWT - SCOPE = internal_user_mgt_create
            await self.validate_token_idp_for_signup(idp_token.access_token)
            # (4) - INVOKE SIGNUP REGISTER

            response = await signup_service.register_in_signup_core(
                url_base=self.env_var.signup_core_service_url,
                data=data,
                access_token=idp_token.access_token)
            return response
        except Exception as e:
            self.logger.error("Unexpected error while preparing or sending request", exc_info=True)
            return HttpResponseSchema(
                status_response=False,
                status_code=500,
                data=None,
                message=f"Unhandled exception: {str(e)}"
            )