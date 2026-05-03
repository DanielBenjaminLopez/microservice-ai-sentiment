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
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("Modelo Gemini iniciado correctamente")
        return model
    except Exception as e:
        logger.error(f"Error al inicializar el modelo Gemini: {e}")
        return None

model = get_gemini_model()

def analyze_sentiment(text):
    """
    Analiza el sentimiento de un texto usando Gemini.
    Retorna: {"label": "positivo|negativo|neutral"}
    """
    global model
    if not text:
        return {"label": "neutral"}
    
    # Intentar re-inicializar si es None (útil cuando la API key se configura después)
    if model is None:
        logger.debug("Modelo es None, intentando reinicializar...")
        model = get_gemini_model()
        
    if model is None:
        logger.error("No es posible analizar sentimiento: API key de Gemini no configurada")
        return {"label": "neutral"}

    prompt = f"Responde solo con una palabra: positivo, negativo o neutral. Texto: {text}"
    
    try:
        response = model.generate_content(prompt)
        label = response.text.strip().lower()
        if label in ['positivo', 'negativo', 'neutral']:
            logger.debug(f"Sentimiento detectado para '{text[:30]}...': {label}")
            return {"label": label}
        logger.warning(f"Respuesta inesperada del modelo: {label}")
        return {"label": "neutral"}
    except Exception as e:
        logger.error(f"Error al analizar sentimiento: {e}")
        return {"label": "neutral"}