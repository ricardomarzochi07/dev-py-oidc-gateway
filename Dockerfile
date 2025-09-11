# Imagen base
FROM python:3.10-slim
USER root
# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=dev

# Instala herramientas necesarias
RUN apt-get update && apt-get install -y build-essential curl

# Crea directorio de trabajo
RUN mkdir -p /app/src/resources
RUN mkdir -p /app/resources
RUN mkdir -p /app/data-report
RUN chmod -R 770 /app/data-report

WORKDIR /app/

# Copia el archivo wheel de la librería
COPY loglib_sca-0.0.1-py3-none-any.whl .

# Copia el resto del código
COPY pyproject.toml /app
COPY main.py /app
COPY /src /app/src
COPY /resources/ /app/resources

# Instala dependencias externas del sistema necesarias (incluyendo Git)
# Instala git y limpia
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instala pip y setuptools actualizados
RUN pip install --upgrade pip setuptools

# Instala la librería desde el .whl
# RUN pip install loglib_sca-0.0.1-py3-none-any.whl

# Instala el resto del proyecto desde el pyproject.toml
RUN pip install .

# Comando para iniciar FastAPI
CMD ["uvicorn", "src.server.app:app", "--host", "0.0.0.0", "--port", "8080"]