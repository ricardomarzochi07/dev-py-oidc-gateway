from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from app.core.environment_config import AppConfig
from app.core.settings_config import load_config
from buddybet_logmon_common.logger import get_logger
from buddybet_transactionmanager.http.transaction_http import HttpResponseSchema
from app.schemas.signupsubmit_request_schema import SignupSubmitRequest
from app.schemas.token_internal_schema import TokenInternalSchema
from app.service.impl.oidc_service_impl import OidcServiceImpl

router = APIRouter()
logger = get_logger()
security = HTTPBearer()


def get_oidc_service(config: AppConfig = Depends(load_config)) -> OidcServiceImpl:
    return OidcServiceImpl(config)


@router.post("/oidc/signup/submit",
             response_model_exclude_none=True,
             summary="Register User",
             response_model=HttpResponseSchema,
             responses={
                 200: {"description": "Success"},
                 401: {"description": "Unauthorized"},
                 502: {"description": "Unavailable"},
             })
async def post_register_user(data: SignupSubmitRequest, oidcService: OidcServiceImpl = Depends(get_oidc_service)):
    logger.info("Execute Request - post_signup_user")
    try:
        tokenInternalResponse = oidcService.orchestrate_signup_user(data)
        return tokenInternalResponse
    except Exception as e:
        logger.error(f"Error Execute Request - internal_token:", exc_info=True)
        return HttpResponseSchema(
            status_response=False,
            status_code=500,
            data=None,
            message=f"Unhandled exception: {str(e)}"
        )