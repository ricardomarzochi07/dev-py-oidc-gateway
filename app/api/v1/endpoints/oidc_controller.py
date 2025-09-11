from fastapi import APIRouter, Body, Depends, Response, Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.environment_config import AppConfig
from app.core.settings_config import load_config
from buddybet_logmon_common.logger import get_logger
from app.schemas.token_schema_response import TokenResponseSchema
from app.service.impl.oidc_service_impl import OidcServiceImpl

router = APIRouter()
logger = get_logger()
security = HTTPBearer()


def get_oidc_service(config: AppConfig = Depends(load_config)) -> OidcServiceImpl:
    return OidcServiceImpl(config)


@router.post("/api/oidc/token-internal",
             response_model_exclude_none=True,
             summary="Return Token JWT > IdP",
             response_model=TokenResponseSchema,
             responses={
                 200: {"description": "Success"},
                 401: {"description": "Unauthorized"},
                 502: {"description": "Unavailable"},
             })
async def internal_token(oidcService: OidcServiceImpl = Depends(get_oidc_service)):
    logger.info("Execute Request - issue_internal_token")
    try:
        tokenResponseSchema = oidcService.generate_token()
        return tokenResponseSchema
    except Exception as e:
        logger.error(f"Error Execute Request - internal_token:", exc_info=True)
        raise HTTPException(status_code=500, detail="Error internal")


@router.post("/api/oidc/token-wso2",
             response_model_exclude_none=True,
             summary="Return Token JWT > IdP",
             response_model=TokenResponseSchema,
             responses={
                 200: {"description": "Success"},
                 401: {"description": "Unauthorized"},
                 502: {"description": "WSO2 Unavailable"},
             })
async def wso2_token(credentials: HTTPAuthorizationCredentials = Depends(security),
                     oidcService: OidcServiceImpl = Depends(get_oidc_service)):
    logger.info("Execute Request - issue_wso2_token")
    try:
        token = credentials.credentials
        print(" TOKENNNNNNNNNNNNNNNNN ========= ", token)
        #oidcService = OidcServiceImpl(config)
        tokenResponseSchema = oidcService.issue_wso2_token(token)
        return tokenResponseSchema
    except Exception as e:
        logger.error(f"Error Execute Request - wso2_token:", exc_info=True)
        raise HTTPException(status_code=500, detail="Error internal")
