import os
import google.generativeai as genai

def analyze_sentiment(text):
    if not text:
        return {"label": "neutral"}
    
    # 1. Intentar obtener la KEY en cada llamada si algo falló al inicio
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return {"label": "error", "detail": "Variable GEMINI_API_KEY no encontrada en el entorno"}

    try:
        # 2. Configuración y modelo
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            "Responde solo con una palabra: positivo, negativo o neutral. "
            f"Texto: {text}"
        )
        
        response = model.generate_content(prompt)
        label = response.text.strip().lower()
        
        if label in ['positivo', 'negativo', 'neutral']:
            return {"label": label}
        return {"label": "neutral", "debug": f"IA respondió: {label}"}

    except Exception as e:
        # 3. VER EL ERROR REAL
        return {"label": "error", "detail": str(e)}