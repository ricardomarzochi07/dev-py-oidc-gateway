class IAMConstants:
    DEFAULT_EXP_MINUTES = 2
    ALGORITHM = "RS256"
    TOKEN_TYPE = "Bearer"
    AUDIENCE = "REGISTER-USER"
    SCOPE = "create:user"
    ISSUER= "https://localhost:8002/oidc-gateway"
    LOCAL_ENV = "local"
    DEV_ENV = "dev"
    PRE_ENV = "pre"
    PROD_ENV = "prod"
