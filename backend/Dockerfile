FROM mcr.microsoft.com/playwright/python:v1.41.1-jammy

WORKDIR /app

# Cliente de Postgres para facilitar carga de schema/diagnóstico
RUN apt-get update \
 && apt-get install -y --no-install-recommends postgresql-client \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ejecuta FastAPI con host público
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
