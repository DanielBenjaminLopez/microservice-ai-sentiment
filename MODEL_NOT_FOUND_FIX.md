# Solución: Modelo Gemini No Disponible

## Problema
El error `404 models/gemini-1.5-flash is not found` indica que el modelo `gemini-1.5-flash` no está disponible en tu API key (probablemente porque es una API key de prueba o tiene restricciones).

## Soluciones Implementadas

### 1. **Cambio de Modelo**
- **Antes**: `gemini-1.5-flash` (no disponible)
- **Ahora**: `gemini-2.0-flash` (modelo más nuevo, más probable que esté disponible)

### 2. **Nuevo Endpoint para Listar Modelos Disponibles**
Accede a: `https://microservice-ai-sentiment.onrender.com/api/list-models/`

Este endpoint te muestra exactamente qué modelos están disponibles en tu API key:
```json
{
  "available_models": [
    {"name": "models/gemini-pro", "display_name": "Gemini Pro"},
    {"name": "models/gemini-pro-vision", "display_name": "Gemini Pro Vision"},
    ...
  ],
  "current_model": "gemini-2.0-flash",
  "total_models": 5
}
```

### 3. **Fallback Automático**
Si `gemini-2.0-flash` tampoco estuviera disponible, la aplicación registrará qué modelos están disponibles en los logs.

## Archivos Modificados

- `classifier/logic.py`
  - Cambio de `gemini-1.5-flash` → `gemini-2.0-flash`
  - Nueva función `list_available_models()` para debugging

- `classifier/views.py`
  - Nuevo endpoint `list_models_view()` en `/api/list-models/`
  - Importa la nueva función de modelos

- `classifier/urls.py`
  - Ruta para `/api/list-models/`

## Próximos Pasos

1. **Haz redeploy en Render**
   - Dashboard → Manual Deploys → Deploy

2. **Verifica que funciona**:
   ```bash
   # Verificar qué modelos están disponibles
   curl https://microservice-ai-sentiment.onrender.com/api/list-models/
   
   # Probar análisis de sentimiento
   curl "https://microservice-ai-sentiment.onrender.com/api/analyze/?text=Estoy%20feliz"
   ```

3. **Si gemini-2.0-flash tampoco funciona**:
   - Accede a `/api/list-models/` para ver qué modelos sí están disponibles
   - Avísame el nombre del modelo que puedes usar
   - Lo cambio automáticamente en el código

## Tests

✅ 8 pytest tests: PASSED
✅ 3 Behave scenarios: PASSED

Todo mantiene compatibilidad.
