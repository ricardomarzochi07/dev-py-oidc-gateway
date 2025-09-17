from fastapi import FastAPI
from app.api import oidc_signup_api, oidc_token_api
from buddybet_logmon_common.fastapi_logger import setup_fastapi_logging
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
setup_fastapi_logging(app)
app.include_router(oidc_token_api.router, prefix="/oidc_token", tags=["oidc-token"])
app.include_router(oidc_signup_api.router, prefix="/oidc_signup", tags=["oidc-token"])

# Configuración CORS si tu frontend está en otro dominio
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],  # ajustar según deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
