import os
import yaml
from functools import lru_cache
from app.core.environment_config import AppConfig, AppConfigEnvironment
from pathlib import Path
import re
from cryptography.hazmat.primitives import serialization

from app.core.oidc_constants import IAMConstants
from app.dto.keys_dto import KeysDTO


def expand_env_variables(content: str) -> str:
    # Reemplaza ${VAR} por el valor real de os.environ["VAR"]
    return re.sub(r'\$\{([^}]+)}', lambda m: os.getenv(m.group(1), ""), content)


@lru_cache()
def load_config():
    app_env = os.getenv("APP_ENV")
    with open(Path(f"resources/env_{app_env}.yaml"), "r") as f:
        content = f.read()

    expand_content = expand_env_variables(content)
    data = yaml.safe_load(expand_content)

    # Cargar keys
    keys = get_keys(app_env)

    # Extraer diccionario interno
    oidc_env_data = data.get("oidc_gateway_env", {}).copy()
    oidc_env_data["public_key"] = keys.public_key
    oidc_env_data["private_key"] = keys.private_key

    # Crear AppConfigEnvironment
    oidc_env = AppConfigEnvironment(**oidc_env_data)

    # Retornar el config completo
    return AppConfig(oidc_gateway_env=oidc_env)

def get_keys(app_env: str):
    match app_env:
        case IAMConstants.LOCAL_ENV:
            return KeysDTO(
                private_key=open_file_private_dev(app_env),
                public_key=open_file_public_dev(app_env))
        case IAMConstants.PRE_ENV:
            print("Env PRE")
            return None
        case IAMConstants.PROD_ENV:
            print("Env PRO")
            return None
        case _:
            raise ValueError(f"Entorno desconocido: {app_env}")


def open_file_private_dev(app_env: str):
    key_path = Path(f"resources/certs/private_key_{app_env}.pem")
    pwd_key_private = os.getenv("JWT_KEY_PASSPHRASE")

    if not pwd_key_private:
        raise ValueError("No se ha definido JWT_KEY_PASSPHRASE en el entorno")
    try:
        with open(key_path, "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=pwd_key_private.encode()  # passphrase de tu PEM
            )
            # Serializar la clave privada a bytes PEM

        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,  # PKCS#1
            encryption_algorithm=serialization.NoEncryption()  # sin cifrado al exportar
        )
        return private_key_bytes
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo de clave privada: {key_path}")
    except ValueError as e:
        raise ValueError(f"Error cargando la clave privada: {e}")


def open_file_public_dev(app_env: str):
    key_path = Path(f"resources/certs/public_key_{app_env}.pem")
    try:
        with open(key_path, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())
            public_key_bytes = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        return public_key_bytes
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo de clave public: {key_path}")
    except ValueError as e:
        raise ValueError(f"Error cargando la clave public: {e}")
