from django.shortcuts import render
from django.http import JsonResponse
from .logic import analyze_sentiment, model
import os
import logging

logger = logging.getLogger(__name__)

def sentiment_view(request):
    text = request.GET.get('text', '')
    result = analyze_sentiment(text)
    return JsonResponse(result)

def debug_view(request):
    """
    Endpoint de debug para diagnosticar problemas con la API de Gemini.
    Solo accesible en modo debug.
    """
    api_key = os.getenv('GEMINI_API_KEY')
    
    debug_info = {
        "api_key_configured": bool(api_key),
        "api_key_length": len(api_key) if api_key else 0,
        "model_initialized": model is not None,
        "model_type": str(type(model)) if model else None,
    }
    
    # Intentar hacer una llamada simple a la API
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