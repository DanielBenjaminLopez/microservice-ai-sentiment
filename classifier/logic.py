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
        # Intenta con gemini-2.5-flash (modelo más nuevo y estable)
        model = genai.GenerativeModel('gemini-2.5-flash')
        logger.info("✓ Modelo Gemini (gemini-2.5-flash) iniciado correctamente")
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

    # Prompt altamente optimizado para respuesta consistente
    prompt = (
        "You are a sentiment analyzer. Analyze the sentiment of the following text and respond with EXACTLY ONE WORD ONLY.\n\n"
        "The response must be one of these three options:\n"
        "- positive (if the text expresses positive sentiment)\n"
        "- negative (if the text expresses negative sentiment)\n"
        "- neutral (if the text is neutral or unclear)\n\n"
        "Do NOT include any explanation, punctuation, or additional text. Only the single word.\n\n"
        f"Text to analyze: {text}\n\n"
        "Response:"
    )
    
    try:
        logger.debug(f"Enviando solicitud a Gemini para texto: '{text[:50]}...'")
        response = model.generate_content(prompt, generation_config={
            "temperature": 0.1,
            "top_p": 0.1,
        })
        
        raw_response = response.text.strip()
        logger.debug(f"[RAW RESPONSE] {repr(raw_response)}")
        
        label = raw_response.lower().strip()
        label = label.replace('"', '').replace("'", '').replace('.', '').replace(',', '').replace('!', '').replace('*', '')
        
        logger.debug(f"[PROCESSED] '{label}'")
        
        if label in ['positive', 'positivo']:
            logger.info(f"✓ POSITIVE detectado para '{text[:30]}...': {label}")
            return {"label": "positivo"}
        elif label in ['negative', 'negativo']:
            logger.info(f"✓ NEGATIVE detectado para '{text[:30]}...': {label}")
            return {"label": "negativo"}
        elif label in ['neutral']:
            logger.info(f"✓ NEUTRAL detectado para '{text[:30]}...': {label}")
            return {"label": "neutral"}
        else:
            logger.warning(f"✗ Respuesta no reconocida: '{raw_response}' -> '{label}'")
            return {"label": "neutral"}
        
    except Exception as e:
        logger.error(f"✗ Error al analizar sentimiento: {type(e).__name__}: {e}", exc_info=True)
        return {"label": "neutral"}