# Dockerfile para despliegue en Fly.io
FROM python:3.11-slim

WORKDIR /app

# Copiar archivos de la app
COPY . .

# Instalar dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Variables de entorno para producción
ENV PYTHONUNBUFFERED=1
ENV PORT=5001

# Exponer el puerto
EXPOSE 5001

# Comando de arranque con gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5001", "app_sommelier:app"]
