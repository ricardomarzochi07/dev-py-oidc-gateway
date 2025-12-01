from buddybet_idpsecure.authorization.transaction_auth import TransactionAuthorization
from buddybet_idpsecure.model.user_claims import UserClaims
from app.core.exceptions import InvalidToken, InvalidScope
from app.core.oidc_constants import Constants
import jwt
from jose import jwt
from jose.exceptions import JWTError
from buddybet_logmon_common.logger import get_logger

logger = get_logger()


def validate_token_internal(internal_token: str, public_key: str, ) -> bool:
    logger.info("Execute Request - validate_internal_token")
    try:
        # Validar JWT interno del broker
        logger.info("Validar Token Interno - issue_wso2_token")
        jwt.decode(internal_token, public_key, algorithms=Constants.ALGORITHM,
                   audience=Constants.AUDIENCE)
        return True
    except JWTError as e:
        logger.error(f"Token inválido: {str(e)}", exc_info=True)
        raise InvalidToken() from e


async def validate_token_idp_for_signup(idp_token: str, idp_scope_signup: str):
    logger.info("Execute Request - validate_token_idp")
    try:
        auth_token = TransactionAuthorization(idp_token)
        user_token: UserClaims = await auth_token.transaction_valid(None)

        if user_token.scope is not None:
            scopes = user_token.scope
            if idp_scope_signup not in scopes:
                logger.error("Scope Inválido", exc_info=True)
                raise InvalidScope()

    except JWTError as e:
        logger.error(f"Token inválido: {str(e)}", exc_info=True)
        raise InvalidToken() from e
