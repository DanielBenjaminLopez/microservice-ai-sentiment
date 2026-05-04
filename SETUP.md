# 📋 Guía de Configuración del Analizador de Sentimiento

## 🎯 Requisitos Previos

- Python 3.12+
- Node.js 16+
- npm o yarn
- Git
- Docker (opcional, para producción)
- Una API key de Google Generative AI (gratis en https://ai.google.dev)

## 🚀 Opción 1: Desarrollo Local (Recomendado para empezar)

### Paso 1: Clonar o descargar el proyecto

```bash
cd /tu/carpeta/del/proyecto
```

### Paso 2: Configurar el Backend (Django + Python)

```bash
# Instalar las dependencias de Python
pip install -r requirements.txt

# Configurar la variable de entorno con tu API key
export GEMINI_API_KEY="tu-api-key-aqui"

# En Windows, usa:
# set GEMINI_API_KEY=tu-api-key-aqui

# Ejecutar migraciones de base de datos
python manage.py migrate

# Iniciar el servidor backend en el puerto 8000
python manage.py runserver
```

**El backend estará disponible en: http://localhost:8000**

### Paso 3: Configurar el Frontend (React + Vite) - En otra terminal

```bash
cd frontend

# Instalar dependencias de Node.js
npm install

# Iniciar el servidor de desarrollo en el puerto 5173
npm run dev
```

**El frontend estará disponible en: http://localhost:5173**

### ¡Listo! 🎉

Ahora puedes:
- Abrir http://localhost:5173 en tu navegador
- Escribir texto y analizar su sentimiento
- El frontend hará peticiones al backend automáticamente

---

## 🐳 Opción 2: Desarrollo con Docker Compose (Más simple)

Esta opción ejecuta tanto backend como frontend en contenedores.

### Paso 1: Configurar la variable de entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
GEMINI_API_KEY=tu-api-key-aqui
```

### Paso 2: Ejecutar con Docker Compose

```bash
# Construir las imágenes y ejecutar los contenedores
docker-compose up

# O en modo background:
docker-compose up -d

# Ver los logs
docker-compose logs -f

# Detener los servicios
docker-compose down
```

**Acceso:**
- Frontend: http://localhost:5173
- Backend: http://localhost:8000

---

## 📦 Opción 3: Despliegue en Producción (Docker - para Render o similar)

### Paso 1: Construir la imagen Docker

Esta imagen incluye tanto el backend como el frontend compilado.

```bash
# Construir la imagen
docker build -t sentiment-analyzer:latest .

# O si estás usando Docker Hub:
docker build -t tuusuario/sentiment-analyzer:latest .
```

### Paso 2: Ejecutar el contenedor

```bash
# Ejecutar localmente
docker run -p 8000:8000 \
  -e GEMINI_API_KEY="tu-api-key-aqui" \
  sentiment-analyzer:latest

# O con docker-compose
docker-compose -f docker-compose.prod.yml up
```

### Paso 3: Despliegue en Render.com

1. Conecta tu repositorio de GitHub con Render
2. Crea un nuevo servicio "Web Service"
3. Selecciona tu repositorio
4. Configuración:
   - **Build Command**: `pip install -r requirements.txt && npm install --prefix frontend && npm run build --prefix frontend`
   - **Start Command**: `python manage.py runserver 0.0.0.0:8000`
   - **Environment Variables**:
     - `GEMINI_API_KEY`: Tu API key
     - `DEBUG=False` (para producción)

---

## 🔧 Comandos Útiles del Frontend

```bash
cd frontend

# Desarrollo
npm run dev

# Construir para producción
npm run build

# Preview de la construcción
npm run preview

# Instalar nuevas dependencias
npm install package-name

# Eliminar node_modules y reinstalar
rm -rf node_modules && npm install
```

## 🔧 Comandos Útiles del Backend

```bash
# Ejecutar servidor
python manage.py runserver

# Ejecutar tests
python manage.py test

# Ejecutar pytest
pytest classifier/tests/test_sentiment.py -v

# Ejecutar tests Behave
behave features/sentiment.feature -v

# Hacer migraciones
python manage.py makemigrations
python manage.py migrate

# Shell interactivo Django
python manage.py shell
```

---

## 🧪 Probar la API Directamente

### Sin frontend - Petición GET simple

```bash
# Analizar sentimiento
curl "http://localhost:8000/api/analyze/?text=Me%20siento%20muy%20feliz"

# Ver información de debug
curl "http://localhost:8000/api/debug/"

# Ver respuesta raw del modelo
curl "http://localhost:8000/api/raw-sentiment/?text=Estoy%20triste"

# Listar modelos disponibles
curl "http://localhost:8000/api/list-models/"
```

### Con Python

```python
import requests

response = requests.get(
    "http://localhost:8000/api/analyze/",
    params={"text": "Me encanta este proyecto"}
)
print(response.json())
```

---

## 🆘 Solucionar Problemas

### "ModuleNotFoundError: No module named 'google.generativeai'"

```bash
pip install -r requirements.txt
```

### "npm ERR! ERESOLVE unable to resolve dependency tree"

```bash
cd frontend
npm install --legacy-peer-deps
```

### El frontend no puede conectar al backend

- Asegúrate de que el backend está corriendo en http://localhost:8000
- En production, configura la URL del backend en las variables de entorno

### GEMINI_API_KEY no reconocida

- Verifica que la variable esté configurada: `echo $GEMINI_API_KEY`
- Reinicia los servidores después de configurarla

---

## 📱 Estructura de Carpetas

```
microservice-ai-sentiment/
├── backend/          # Código Django
│   ├── classifier/   # App principal
│   ├── core/         # Configuración Django
│   ├── manage.py
│   ├── requirements.txt
│   └── db.sqlite3
├── frontend/         # Código React + Vite
│   ├── src/
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── dist/         # Build final (generado)
├── Dockerfile        # Para multi-stage build (frontend + backend)
├── Dockerfile.frontend  # Solo frontend
├── docker-compose.yml   # Orquestación local
└── SETUP.md          # Este archivo
```

---

## ✅ Checklist de Configuración

- [ ] Python 3.12+ instalado
- [ ] Node.js 16+ instalado
- [ ] API key de Google Generative AI obtenida
- [ ] Dependencias de Python instaladas (`pip install -r requirements.txt`)
- [ ] Dependencias de Node instaladas (`cd frontend && npm install`)
- [ ] Variable GEMINI_API_KEY configurada
- [ ] Backend corriendo sin errores en puerto 8000
- [ ] Frontend corriendo sin errores en puerto 5173
- [ ] Puedes acceder a http://localhost:5173 desde el navegador
- [ ] Puedes analizar sentimientos sin errores

---

## 🚀 Próximos Pasos

1. **Desarrollo local**: Usa Opción 1 para editar código
2. **Testing**: Ejecuta `pytest` y `behave` antes de hacer push
3. **Despliegue**: Usa Opción 3 con Docker para llevar a producción
4. **Monitoreo**: Usa los endpoints de debug para troubleshooting

---

## 📚 Recursos

- [Google Generative AI Docs](https://ai.google.dev)
- [Django Docs](https://docs.djangoproject.com/)
- [React Docs](https://react.dev)
- [Vite Docs](https://vitejs.dev)
- [Docker Docs](https://docs.docker.com/)

---

¡Que disfrutes analizando sentimientos! 🎉✨
