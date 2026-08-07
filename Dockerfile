# ---------------------------------------------------
# ETAPA 1: Builder (Compilación e instalación)
# ---------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /app

# Instalar herramientas de compilación temporales
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Crear entorno virtual aislado
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------------------------------------------------
# ETAPA 2: Runner (Imagen final limpia de producción)
# ---------------------------------------------------
FROM python:3.12-slim AS runner

WORKDIR /app

# Copiar el entorno virtual ya compilado desde la etapa builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar el código fuente de la aplicación
COPY app/ ./app

# Seguridad: Usuario no-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 10000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]