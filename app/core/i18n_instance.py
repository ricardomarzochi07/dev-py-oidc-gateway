import os
from buddybet_i18n.i18n_service import I18nService
from pathlib import Path


def find_resources_folder(start_path=None):
    # Si no se pasa un start_path, tomar el directorio actual
    start_path = start_path or Path(__file__).resolve()

    # Subir hasta encontrar la carpeta 'resources'
    while start_path != start_path.root:
        resources_path = start_path / 'resources'
        if resources_path.exists() and resources_path.is_dir():
            return resources_path
        start_path = start_path.parent

    raise FileNotFoundError("No se encontró la carpeta 'resources' en el proyecto")


# Configuración del directorio de recursos
dir_resources = find_resources_folder()

# Inicializar I18nService
i18n = I18nService(root_dir=dir_resources)
