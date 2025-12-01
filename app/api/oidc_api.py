from buddybet_transactionmanager.schemas.http_response_schema import HttpResponseSchema
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from app.core.environment_config import AppConfig
from app.core.exceptions import UserRegistration, GenerateInternalToken
from app.core.exceptions_handlers import build_success_response
from app.core.settings_config import load_config
from buddybet_logmon_common.logger import get_logger
from app.core.cache.factory_cache import get_cache
from app.schemas.signin_init_request_schema import SigninRequestSchema
from app.schemas.signin_init_response_schema import SigninResponseSchema
from app.schemas.signupsubmit_request_schema import SignupSubmitRequest
from app.schemas.token_internal_schema import TokenInternalSchema
from app.service.impl.oidc_service_impl import OidcServiceImpl
from app.core.cache.base import Cache

router = APIRouter()
logger = get_logger()
security = HTTPBearer()


# Provider do serviço (injeção de dependências)
def get_oidc_service(
        config: AppConfig = Depends(load_config),  # FastAPI injeta AppConfig
        cache: Cache = Depends(get_cache),  # FastAPI injeta Cache (que já recebeu AppConfig)
) -> OidcServiceImpl:
    return OidcServiceImpl(config=config, cache=cache)


@router.get(
    "/token/internal",
    response_model_exclude_none=True,
    summary="Return Token JWT > IdP",
    response_model=HttpResponseSchema[TokenInternalSchema],
    responses={
        200: {"description": "Success"},
        401: {"description": "Unauthorized"},
        500: {"description": "Unavailable"},
    },
    # Se quiser exigir Authorization: Bearer <token>, descomente:
    # dependencies=[Depends(security)],
)
async def get_token_internal(
        oidc_service: OidcServiceImpl = Depends(get_oidc_service),
):
    logger.info("Execute Request - issue_internal_token")
    # Se for assíncrono:
    # token_internal_resp = await oidc_service.generate_token_internal()
    # Se for síncrono:
    token_internal_resp = oidc_service.generate_token_internal()
    return build_success_response(e=GenerateInternalToken, data=token_internal_resp)


@router.post(
    "/signup/submit",
    response_model_exclude_none=True,
    summary="Register User",
    response_model=HttpResponseSchema,  # se tiver genérico, pode tipar com HttpResponseSchema[SeuDTO]
    responses={
        200: {"description": "Success"},
        401: {"description": "Unauthorized"},
        502: {"description": "WSO2 Unavailable"},
        500: {"description": "Internal Server Error"},
    },
)
async def post_register_user(
        data: SignupSubmitRequest,
        oidc_service: OidcServiceImpl = Depends(get_oidc_service),
):
    logger.info("Execute Request - post_signup_user")
    response = await oidc_service.orchestrate_signup_user(data)
    return build_success_response(e=UserRegistration, data=response)


@router.post(
    "/signin/auth/init",
    response_model_exclude_none=True,
    summary="Register User",
    response_model=HttpResponseSchema[SigninResponseSchema],
    responses={
        200: {"description": "Success"},
        401: {"description": "Unauthorized"},
        502: {"description": "WSO2 Unavailable"},
        500: {"description": "Internal Server Error"},
    },
)
async def post_signin_init(
        data: SigninRequestSchema,
        oidc_service: OidcServiceImpl = Depends(get_oidc_service),
):
    logger.info("Execute Request - post_signup_user")
    response = await oidc_service.orchestrate_signin_user(data=data)
    return build_success_response(e=UserRegistration, data=response)
