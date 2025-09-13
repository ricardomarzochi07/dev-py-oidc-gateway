from fastapi import APIRouter, Body, Depends, Response, Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.environment_config import AppConfig
from app.core.settings_config import load_config
from buddybet_logmon_common.logger import get_logger

from app.schemas.token_idp_schema import TokenIdpSchema
from app.schemas.token_internal_schema import TokenInternalSchema
from app.service.impl.oidc_service_impl import OidcServiceImpl

router = APIRouter()
logger = get_logger()
security = HTTPBearer()


def get_oidc_service(config: AppConfig = Depends(load_config)) -> OidcServiceImpl:
    return OidcServiceImpl(config)


@router.post("/oidc/internal/token",
             response_model_exclude_none=True,
             summary="Return Token JWT > IdP",
             response_model=TokenInternalSchema,
             responses={
                 200: {"description": "Success"},
                 401: {"description": "Unauthorized"},
                 502: {"description": "Unavailable"},
             })
async def get_token_internal(oidcService: OidcServiceImpl = Depends(get_oidc_service)):
    logger.info("Execute Request - issue_internal_token")
    try:
        tokenInternalResponse = oidcService.generate_token_internal()
        return tokenInternalResponse
    except Exception as e:
        logger.error(f"Error Execute Request - internal_token:", exc_info=True)
        raise HTTPException(status_code=500, detail="Error internal")


@router.post("/oidc/idp/token",
             response_model_exclude_none=True,
             summary="Return Token JWT > IdP",
             response_model=TokenIdpSchema,
             responses={
                 200: {"description": "Success"},
                 401: {"description": "Unauthorized"},
                 502: {"description": "WSO2 Unavailable"},
             })
async def get_token_idp(data_token: TokenInternalSchema,
                        oidcService: OidcServiceImpl = Depends(get_oidc_service)):
    logger.info("Execute Request - issue_wso2_token")
    try:
        print(" TOKEN >>> ", data_token.jwt_nonce)
        tokenResponseSchema = oidcService.generate_idp_token(data_token.jwt_nonce)
        return tokenResponseSchema
    except Exception as e:
        logger.error(f"Error Execute Request - wso2_token:", exc_info=True)
        raise HTTPException(status_code=500, detail="Error internal")
