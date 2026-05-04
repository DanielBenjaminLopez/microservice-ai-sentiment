# Analizador de Sentimiento - Frontend

Una interfaz web minimalista y elegante para analizar el sentimiento de textos usando Google Gemini AI.

## 🚀 Características

- ✨ Diseño moderno y minimalista
- 🎨 Interfaz responsiva y accesible
- 🚀 Construcción rápida con Vite
- ⚡ Experiencia de usuario fluida
- 🎯 Integración con API backend
- 📱 Completamente responsive

## 📋 Requisitos

- Node.js 16+ 
- npm o yarn

## 🔧 Instalación

```bash
cd frontend
npm install
```

## 🏃 Desarrollo Local

```bash
npm run dev
```

La aplicación estará disponible en `http://localhost:5173`

**Asegúrate de que el backend esté corriendo en `http://localhost:8000`**

## 🔨 Construcción para Producción

```bash
npm run build
```

Los archivos compilados se guardarán en la carpeta `../static`

## 📚 Estructura del Proyecto

```
frontend/
├── src/
│   ├── App.jsx          # Componente principal
│   ├── App.css          # Estilos
│   └── main.jsx         # Entrada de React
├── index.html           # HTML raíz
├── vite.config.js       # Configuración de Vite
├── package.json         # Dependencias
└── .gitignore          # Archivos ignorados por Git
```

## 🎨 Diseño

- **Minimalista**: Interfaz limpia sin distracciones
- **Gradientes suaves**: Uso de paleta de colores moderna
- **Animaciones**: Transiciones suaves para mejor UX
- **Responsive**: Se adapta a cualquier tamaño de pantalla
- **Accesible**: Semántica HTML y contraste adecuado

## 🔌 Integración con Backend

El frontend se comunica con el backend a través de:

- **Endpoint**: `/api/analyze/?text=...`
- **Método**: GET
- **Respuesta**: JSON con `label` ("positivo", "negativo", "neutral")

### Configuración de Proxy

Vite está configurado para hacer proxy de las peticiones a `/api/` al backend en `http://localhost:8000`.

## 📦 Dependencias Principales

- **React 18.2.0** - Librería UI
- **Vite 4.3.9** - Bundler rápido
- **@vitejs/plugin-react** - Plugin React para Vite

## 🚀 Despliegue

Ver el README principal para instrucciones de despliegue con Docker.

---

Hecho con ❤️ para analizar sentimientos
