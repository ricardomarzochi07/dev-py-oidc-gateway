from fastapi import FastAPI, Request
from app.api import oidc_api
from buddybet_logmon_common.fastapi_logger import setup_fastapi_logging
from fastapi.middleware.cors import CORSMiddleware

from app.core.exceptions_handlers import register_exception_handlers
from app.core.i18n_instance import i18n
from starlette.middleware.base import BaseHTTPMiddleware

# Crear instancia de FastAPI
app = FastAPI()



# Configurar logging
setup_fastapi_logging(app)

# Incluir router de oidc
app.include_router(oidc_api.router, prefix="/oidc_gateway", tags=["oidc-token"])


# Middleware para establecer el idioma en cada request
class LanguageMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Detectar idioma desde el header Accept-Language (o usar 'en' como predeterminado)
        lang = request.headers.get("Accept-Language", "en").split(",")[0]
        i18n.set_language(lang)  # Establecer el idioma en el servicio I18n
        response = await call_next(request)
        return response


# Agregar el middleware a la app
app.add_middleware(LanguageMiddleware)

# Crear instancia de Exception Handlers
register_exception_handlers(app)

# Configuración CORS si tu frontend está en otro dominio
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],  # Ajustar según deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
