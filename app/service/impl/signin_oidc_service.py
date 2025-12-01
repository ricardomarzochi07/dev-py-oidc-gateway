from buddybet_logmon_common.logger import get_logger
from app.core.environment_config import AppConfig
from app.core.cache.factory_cache import get_cache, shutdown_cache


class SigninServiceImpl:
    logger = get_logger()

    def __init__(self, config: AppConfig):
        self.env_var = config.oidc_gateway_env
        self.cache = get_cache(self.env_var)
"""
import time, uuid

PRELOGIN_TTL_SECONDS = 180

def create_prelogin_and_authorize_url(
    client_id: str,
    issuer_authorize: str,
    redirect_uri: str,
    scope: str,
    locale: str | None,
    client_hint: str | None,
    # session_context recebido do Facade (jwt_nonce, jwt_csrf, captcha_token)
    session_context: dict | None,
    prelogin_store,  # ex.: Redis client
):
    # 1) Artefatos OIDC/PKCE
    state = gen_state()
    nonce = gen_nonce()
    code_verifier = gen_code_verifier()
    code_challenge = gen_code_challenge_s256(code_verifier)

    # 2) Persistir pré-login (uso único, TTL curto)
    prelogin_id = "pl_" + uuid.uuid4().hex
    prelogin_store.setex(  # Redis: key, ttl, value
        prelogin_id, PRELOGIN_TTL_SECONDS,
        {
            "state": state,
            "nonce": nonce,
            "code_verifier": code_verifier,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "client_hint": client_hint,
            "locale": locale,
            "created_at": int(time.time()),
            # opcional: guardar só para auditoria/correlação (sem PII)
            "session_context": {
                "has_csrf": bool(session_context and session_context.get("jwt_csrf")),
                "has_captcha": bool(session_context and session_context.get("captcha_token")),
            },
        }
    )

    # 3) Construir URL de autorização
    authorize_url = build_authorize_url(
        issuer_authorize=issuer_authorize,
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=scope,
        state=state,
        nonce=nonce,
        code_challenge=code_challenge,
    )

    # (Opcional) mapear locale/hint para parâmetros do WSO2:
    # - ui_locales=pt
    # - acr_values=...
    # - login_hint=...
    # Se usar, acrescente ao querystring de authorize_url.

    return {
        "authorize_url": authorize_url,
        "prelogin_id": prelogin_id
    }

"""












