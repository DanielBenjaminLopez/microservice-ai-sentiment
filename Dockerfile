# Stage 1: Construir el frontend React con Vite
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./

RUN npm ci

COPY frontend/ .

RUN npm run build

# Stage 2: Aplicación Django con archivos estáticos del frontend
FROM python:3.12-slim

# Evitar que Python escriba archivos .pyc y permitir logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto (excepto frontend)
COPY . .

# Copiar los archivos estáticos construidos del frontend
COPY --from=frontend-builder /app/frontend/dist ./static/dist

# Exponer el puerto que usa Django
EXPOSE 8000

# Comando para arrancar la app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]