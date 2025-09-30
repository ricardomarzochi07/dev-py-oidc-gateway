from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from app.core.environment_config import AppConfig
from app.core.exceptions import UserRegistration, GenerateInternalToken
from app.core.exceptions_handlers import build_success_response
from app.core.settings_config import load_config
from buddybet_logmon_common.logger import get_logger
from app.schemas.signupsubmit_request_schema import SignupSubmitRequest
from app.schemas.token_idp_schema import TokenIdpSchema
from app.schemas.token_internal_schema import TokenInternalSchema
from app.service.impl.oidc_service_impl import OidcServiceImpl
from buddybet_transactionmanager.http.transaction_http import HttpResponseSchema

router = APIRouter()
logger = get_logger()
security = HTTPBearer()


def get_oidc_service(config: AppConfig = Depends(load_config)) -> OidcServiceImpl:
    return OidcServiceImpl(config)


@router.get("/token/internal",
            response_model_exclude_none=True,
            summary="Return Token JWT > IdP",
            response_model=HttpResponseSchema[TokenInternalSchema],
            responses={
                200: {"description": "Success"},
                401: {"description": "Unauthorized"},
                500: {"description": "Unavailable"},
            })
async def get_token_internal(oidcService: OidcServiceImpl = Depends(get_oidc_service)):
    logger.info("Execute Request - issue_internal_token")
    token_internal_resp = oidcService.generate_token_internal()
    return build_success_response(e=GenerateInternalToken, data=token_internal_resp)




@router.post("/token/idp",
             response_model_exclude_none=True,
             response_model=HttpResponseSchema[TokenIdpSchema],
             responses={
                 200: {"description": "Success"},
                 401: {"description": "Unauthorized"},
                 502: {"description": "WSO2 Unavailable"},
                 500: {"description": "Internal Server Error"},
             })
async def get_token_idp(data_token: TokenInternalSchema,
                        oidcService: OidcServiceImpl = Depends(get_oidc_service)):
    logger.info("Execute Request - issue_wso2_token")
    resp_token_idp = await oidcService.generate_idp_token(data_token.jwt_nonce)
    return build_success_response(e=GenerateInternalToken, data=resp_token_idp)


@router.post("/signup/submit",
             response_model_exclude_none=True,
             summary="Register User",
             response_model=HttpResponseSchema,
             responses={
                 200: {"description": "Success"},
                 401: {"description": "Unauthorized"},
                 502: {"description": "WSO2 Unavailable"},
                 500: {"description": "Internal Server Error"},
             })
async def post_register_user(data: SignupSubmitRequest, oidcService: OidcServiceImpl = Depends(get_oidc_service)):
    logger.info("Execute Request - post_signup_user")
    response = await oidcService.orchestrate_signup_user(data)
    return build_success_response(e=UserRegistration, data=response)
