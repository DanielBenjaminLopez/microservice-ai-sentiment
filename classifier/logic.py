import os
import google.generativeai as genai

# Configuración global para no repetir trabajo
def configure_genai():
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')
    return None

# Instanciamos el modelo una sola vez al cargar el módulo
model = configure_genai()

def analyze_sentiment(text):
    if not text or not model:
        return {"label": "neutral"}
    
    prompt = (
        "Analiza el sentimiento del siguiente texto y responde "
        "únicamente con una palabra en minúsculas: 'positivo', 'negativo' o 'neutral'. "
        f"Texto: {text}"
    )
    
    try:
        response = model.generate_content(prompt)
        # El strip() es vital por si la IA agrega espacios o saltos de línea
        label = response.text.strip().lower()
        
        if label in ['positivo', 'negativo', 'neutral']:
            return {"label": label}
        return {"label": "neutral"}
    except Exception:
        # En producción, aquí deberías loguear el error real
        return {"label": "neutral"}