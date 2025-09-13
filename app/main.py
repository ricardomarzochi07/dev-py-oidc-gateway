from fastapi import FastAPI
from app.api.v1.endpoints import oidc_api
from buddybet_logmon_common.fastapi_logger import setup_fastapi_logging
from fastapi.middleware.cors import CORSMiddleware
import os


app = FastAPI()
setup_fastapi_logging(app)
app.include_router(oidc_api.router, prefix="/oidc_gateway", tags=["oidc-gateway"])

# Configuración CORS si tu frontend está en otro dominio
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],  # ajustar según deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
