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

### 1. Endpoint de Debug
Primero, diagnostica el problema accediendo al endpoint de debug:

```
https://microservice-ai-sentiment.onrender.com/api/debug/
```

Este endpoint retornará información como:
```json
{
  "api_key_configured": true,
  "api_key_length": 39,
  "model_initialized": true,
  "model_type": "<class 'google.generativeai.generative_model.GenerativeModel'>",
  "api_test": "SUCCESS",
  "test_response": "Test response successful"
}
```

**Interpretación:**
- ✅ Si `api_key_configured: true` y `model_initialized: true` → API key está bien
- ✅ Si `api_test: "SUCCESS"` → La API de Gemini responde correctamente
- ❌ Si `api_test: "FAILED"` → Hay un problema con la API (lee el `api_error`)

### 2. Endpoint de Análisis
Una vez verificado el debug, prueba el análisis:

```
https://microservice-ai-sentiment.onrender.com/api/analyze/?text=Estoy%20muy%20feliz
```

Deberías obtener una respuesta como:
```json
{"label": "positivo"}
```

## Solucionar Problemas

### Siempre devuelve "neutral"

**Paso 1: Verifica el endpoint de debug**
- Si `api_key_configured: false` → La variable de entorno no está configurada
- Si `model_initialized: false` → Hay un error al inicializar el modelo (lee los logs)
- Si `api_test: "FAILED"` → Problema con la API de Gemini

**Paso 2: Revisa los logs de Render**
- Ve a "Logs" en el panel de Render
- Busca mensajes con `✗` o `ERROR`
- Los errores más comunes:
  - `INVALID_ARGUMENT` → API key inválida
  - `RESOURCE_EXHAUSTED` → Has superado tu cuota de solicitudes
  - `PERMISSION_DENIED` → La API key no tiene permisos

**Paso 3: Redeploy**
- Si acabas de configurar `GEMINI_API_KEY`, necesitas hacer un redeploy manual
- Ve a "Manual Deploys" y haz clic en "Deploy"

## Logs

Puedes ver los logs en Render para debugging. La aplicación registra:
- `✓` = Operación exitosa
- `✗` = Error o problema
- `DEBUG` = Información detallada

Los logs te ayudarán a diagnosticar exactamente qué está pasando.
