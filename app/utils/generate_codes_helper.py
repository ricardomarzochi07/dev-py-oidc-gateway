import secrets, hashlib, base64
from app.dto.oidc_pkce_dto import OidcPkceDTO


# ---- Helpers de codificação ----

def generate_codes_signin() -> OidcPkceDTO:
    state = _gen_state()
    nonce = _gen_nonce()
    code_verifier = _gen_code_verifier()
    code_challenge = _gen_code_challenge_s256(code_verifier)
    return OidcPkceDTO(state=state, nonce=nonce, code_verifier=code_verifier, code_challenge=code_challenge)


def _b64url_no_pad(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


# ---- Geração de artefatos ----
def _gen_state(nbytes: int = 16) -> str:  # 128 bits
    return _b64url_no_pad(secrets.token_bytes(nbytes))


def _gen_nonce(nbytes: int = 16) -> str:  # 128 bits
    return _b64url_no_pad(secrets.token_bytes(nbytes))


# RFC 7636: 43–128 chars; usamos 64 bytes de entropia -> ~86 chars URL-safe
PKCE_VERIFIER_ALLOWED = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~"


def _gen_code_verifier(nbytes: int = 64) -> str:
    # Gera bytes aleatórios e mapeia para o charset permitido
    raw = secrets.token_bytes(nbytes)
    verifier = []
    for b in raw:
        verifier.append(PKCE_VERIFIER_ALLOWED[b % len(PKCE_VERIFIER_ALLOWED)])
    s = "".join(verifier)
    # Garantir tamanho entre 43 e 128
    return s[:86]  # ~86 é um bom tamanho; ajuste se quiser


def _gen_code_challenge_s256(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode()).digest()
    return _b64url_no_pad(digest)


