# Diagnóstico y Solución: Sentimiento siempre "neutral"

## Problema Identificado

Aunque la API key estaba configurada en Render, el servicio siempre devolvía `"neutral"` sin importar el texto.

**Causa raíz**: Falta de logging detallado para debuguear qué estaba pasando.

## Soluciones Implementadas

### 1. **Endpoint de Debug** (`/api/debug/`)
Nuevo endpoint que te permite diagnosticar el problema:

```bash
curl https://microservice-ai-sentiment.onrender.com/api/debug/
```

**Retorna información como:**
```json
{
  "api_key_configured": true,
  "api_key_length": 39,
  "model_initialized": true,
  "api_test": "SUCCESS"
}
```

**¿Qué verificar?**
- ✅ Si `api_key_configured: true` → La variable de entorno está configurada
- ✅ Si `model_initialized: true` → El modelo se inicializó correctamente
- ✅ Si `api_test: "SUCCESS"` → La API de Gemini responde

Si alguno es falso o FAILED, sabrás exactamente dónde está el problema.

### 2. **Logging Mejorado en `logic.py`**
Ahora registra:
- `✓` = Operación exitosa (visible en logs)
- `✗` = Error (visible en logs)
- Detalles de qué responde la API
- Stack traces completos para excepciones

**Accede a los logs en Render**:
- Dashboard → Tu app → "Logs"

### 3. **Prompt Mejorado**
El prompt ahora es más explícito para asegurar que Gemini responda correctamente.

## Posibles Problemas y Soluciones

### ❌ `api_test: "FAILED"` → Error con la API

**Soluciones**:
1. Verifica que la API key sea válida
2. Comprueba si la cuenta de Google tiene cuotas disponibles
3. Revisa el error específico en logs de Render

### ❌ `api_key_configured: false` → Variable de entorno no está

**Soluciones**:
1. En Render Dashboard, ve a "Environment"
2. Agrega `GEMINI_API_KEY` = tu_clave
3. Haz clic en "Save"
4. Renderizará automáticamente (o haz redeploy manual)

### ✅ Debug OK pero sigue devolviendo neutral

**Próximas cosas a verificar**:
1. Revisa los logs en Render para mensajes `✗`
2. El modelo podría tener rate limiting
3. Intenta con un texto diferente
4. Comprueba que el formato de respuesta sea correcto

## Cómo Hacer Redeploy Manual

Si realizaste cambios en variables de entorno:

1. Ve a Render Dashboard
2. Selecciona tu app
3. Haz clic en "Manual Deploys"
4. Haz clic en "Deploy"

## Archivos Modificados

- `classifier/logic.py` — Logging mejorado, prompt mejor
- `classifier/views.py` — Nuevo endpoint `/api/debug/`
- `classifier/urls.py` — Ruta para el endpoint de debug
- `RENDER_DEPLOYMENT.md` — Guía actualizada con troubleshooting
