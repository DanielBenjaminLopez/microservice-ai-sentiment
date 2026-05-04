import os
import logging
import google.generativeai as genai

# Configurar logging
logger = logging.getLogger(__name__)

def get_gemini_model():
    """
    Inicializa y retorna el modelo de Gemini.
    Retorna None si no hay API key configurada o si hay error.
    """
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        logger.warning("GEMINI_API_KEY no está configurada. Configure esta variable de entorno para usar la API.")
        return None
    
    logger.info(f"Intentando inicializar Gemini con API key (primeros 20 chars): {api_key[:20]}...")
    
    try:
        genai.configure(api_key=api_key)
        # Intenta con gemini-2.0-flash primero (modelo más nuevo)
        model = genai.GenerativeModel('gemini-2.0-flash')
        logger.info("✓ Modelo Gemini (gemini-2.0-flash) iniciado correctamente")
        return model
    except Exception as e:
        logger.error(f"✗ Error al inicializar el modelo Gemini: {type(e).__name__}: {e}")
        logger.info("Intenta acceder a /api/list-models/ para ver modelos disponibles")
        return None

model = get_gemini_model()

def list_available_models():
    """
    Lista todos los modelos disponibles en la API de Gemini.
    Útil para debugging.
    """
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return []
    
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        available = []
        for m in models:
            available.append({
                "name": m.name,
                "display_name": m.display_name,
            })
        return available
    except Exception as e:
        logger.error(f"Error al listar modelos: {e}")
        return []

def analyze_sentiment(text):
    """
    Analiza el sentimiento de un texto usando Gemini.
    Retorna: {"label": "positivo|negativo|neutral"}
    """
    global model
    if not text:
        logger.debug("Texto vacío recibido")
        return {"label": "neutral"}
    
    # Intentar re-inicializar si es None (útil cuando la API key se configura después)
    if model is None:
        logger.info("Modelo es None, intentando reinicializar...")
        model = get_gemini_model()
        
    if model is None:
        logger.error("✗ No es posible analizar sentimiento: API key de Gemini no configurada o inválida")
        return {"label": "neutral"}

    # Prompt más explícito y directo
    prompt = (
        "Clasifica el sentimiento del siguiente texto en exactamente una palabra: "
        "'positivo', 'negativo' o 'neutral'. "
        "Responde SOLO la palabra, sin explicaciones ni puntuación adicional. "
        f"Texto a analizar: {text}"
    )
    
    try:
        logger.debug(f"Enviando solicitud a Gemini para texto: '{text[:50]}...'")
        response = model.generate_content(prompt)
        label = response.text.strip().lower()
        
        logger.debug(f"Respuesta bruta de Gemini: '{response.text}'")
        logger.debug(f"Respuesta procesada: '{label}'")
        
        if label in ['positivo', 'negativo', 'neutral']:
            logger.info(f"✓ Sentimiento detectado para '{text[:30]}...': {label}")
            return {"label": label}
        
        logger.warning(f"✗ Respuesta inesperada del modelo: '{label}' (no coincide con valores válidos)")
        return {"label": "neutral"}
        
    except Exception as e:
        logger.error(f"✗ Error al analizar sentimiento: {type(e).__name__}: {e}", exc_info=True)
        return {"label": "neutral"}