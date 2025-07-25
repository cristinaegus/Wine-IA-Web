# Dockerfile para despliegue seguro en Fly.io
FROM python:3.11.8-slim-bookworm

# Actualizar paquetes del sistema para mitigar vulnerabilidades
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Crear usuario no root
RUN useradd -m appuser

WORKDIR /app

# Copiar solo requirements primero para aprovechar cache
COPY requirements.txt ./

# Instalar dependencias del sistema necesarias y limpiar
RUN apt-get update && \
	apt-get install -y --no-install-recommends gcc && \
	pip install --upgrade pip && \
	pip install --no-cache-dir -r requirements.txt && \
	apt-get purge -y --auto-remove gcc && \
	rm -rf /var/lib/apt/lists/* && \
	pip check

# Copiar el resto de la app
COPY . .

ENV PYTHONUNBUFFERED=1
ENV PORT=5001

USER appuser

EXPOSE 5001

CMD ["gunicorn", "-b", "0.0.0.0:5001", "app_sommelier:app"]
