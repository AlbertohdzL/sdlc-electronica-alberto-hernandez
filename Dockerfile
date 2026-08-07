# 1. Imagen base liviana oficial de Python
FROM python:3.12-slim

# 2. Evita la creación de archivos .pyc y fuerza la salida de logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiar e instalar dependencias PRIMERO para aprovechar la caché de capas de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copiar el código de la aplicación
COPY . .

# 6. Exponer el puerto donde corre la API
EXPOSE 8000

# 7. Comando de arranque usando la sintaxis de lista de ejecución (exec form)
CMD ["sh", "-c","uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]