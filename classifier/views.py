from django.shortcuts import render
from django.http import JsonResponse
from .logic import analyze_sentiment, model, list_available_models
import os
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)

def sentiment_view(request):
    text = request.GET.get('text', '')
    result = analyze_sentiment(text)
    return JsonResponse(result)

def debug_view(request):
    """
    Endpoint de debug para diagnosticar problemas con la API de Gemini.
    """
    api_key = os.getenv('GEMINI_API_KEY')
    
    debug_info = {
        "api_key_configured": bool(api_key),
        "api_key_length": len(api_key) if api_key else 0,
        "model_initialized": model is not None,
        "model_type": str(type(model)) if model else None,
    }
    
    if model is not None:
        try:
            test_response = model.generate_content("Responde con 'test'")
            debug_info["api_test"] = "SUCCESS"
            debug_info["test_response"] = test_response.text[:100]
        except Exception as e:
            debug_info["api_test"] = "FAILED"
            debug_info["api_error"] = str(e)
    else:
        debug_info["api_test"] = "SKIPPED - model is None"
    
    return JsonResponse(debug_info)

def raw_sentiment_view(request):
    """
    Endpoint para ver la respuesta RAW del modelo sin procesamiento.
    Útil para debugging cuando devuelve neutral.
    """
    text = request.GET.get('text', '')
    
    if not text:
        return JsonResponse({"error": "Parámetro 'text' requerido"}, status=400)
    
    if model is None:
        return JsonResponse({"error": "Modelo no inicializado"}, status=500)
    
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
        response = model.generate_content(prompt, generation_config={
            "temperature": 0.1,
            "top_p": 0.1,
        })
        
        raw_text = response.text
        
        return JsonResponse({
            "text": text,
            "raw_response": raw_text,
            "raw_response_repr": repr(raw_text),
            "stripped": raw_text.strip(),
            "lower_stripped": raw_text.strip().lower(),
            "cleaned": raw_text.strip().lower().replace('"', '').replace("'", '').replace('.', '').replace(',', '').replace('!', '').replace('*', ''),
        })
    except Exception as e:
        return JsonResponse({
            "error": str(e),
            "error_type": type(e).__name__
        }, status=500)

def list_models_view(request):
    """
    Endpoint para listar todos los modelos disponibles en la API.
    """
    models = list_available_models()
    return JsonResponse({
        "available_models": models,
        "current_model": "gemini-2.5-flash",
        "total_models": len(models)
    })