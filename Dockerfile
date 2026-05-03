# 1. Imagen base de Python ligera
# A esto (Python 3.12):
FROM python:3.12-slim

# 2. Evitar que Python escriba archivos .pyc y permitir logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev && rm -rf /var/lib/apt/lists/*

# 5. Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar el resto del código del proyecto
COPY . .

# 7. Exponer el puerto que usa Django
EXPOSE 8000

# 8. Comando para arrancar la app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]