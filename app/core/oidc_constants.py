class Constants:
    DEFAULT_EXP_MINUTES = 2
    ALGORITHM = "RS256"
    TOKEN_TYPE = "Bearer"
    AUDIENCE = "SignupUser"
    SCOPE_SIGNUP_IDP = "internal_user_mgt_create"
    SCOPE_INTERNAL = "Signup-initial"
    ISSUER= "https://localhost:8002/oidc-gateway"
    LOCAL_ENV = "local"
    DEV_ENV = "dev"
    PRE_ENV = "pre"
    PROD_ENV = "prod"
    RETRIES = 3
    DELAY = 2.0

