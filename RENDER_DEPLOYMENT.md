# Instrucciones de Deployment en Render

## Variables de Entorno Requeridas

Debes configurar las siguientes variables de entorno en Render:

### 1. **GEMINI_API_KEY** (REQUERIDA)
- **Descripción**: Clave de API de Google Generative AI
- **Cómo obtenerla**:
  1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
  2. Crea un proyecto (o selecciona uno existente)
  3. Habilita la API de "Google Generative AI"
  4. Ve a "Credentials" y crea una nueva API key
  5. Copia la clave

### 2. **DEBUG** (Opcional)
- **Valor recomendado en producción**: `False`
- **Valor actual**: `True`

## Pasos para Configurar en Render

1. Ve a tu aplicación en Render Dashboard
2. Haz clic en "Environment"
3. Agrega las variables:
   - Key: `GEMINI_API_KEY`
   - Value: `tu_api_key_aqui` (sin comillas)
4. Haz clic en "Save"
5. Tu aplicación se redesplegará automáticamente

## Verificar que Funciona

Una vez desplegado, prueba el endpoint:

```
https://microservice-ai-sentiment.onrender.com/api/analyze/?text=Estoy%20muy%20feliz
```

Deberías obtener una respuesta como:
```json
{"label": "positivo"}
```

Si ves `{"label": "neutral"}` para todos los textos, probablemente:
- ❌ `GEMINI_API_KEY` no está configurada
- ❌ La API key es inválida
- ❌ La API key no tiene permisos para usar Gemini

## Logs

Puedes ver los logs en Render para debugging. Si hay errores con la API, aparecerán allí.
