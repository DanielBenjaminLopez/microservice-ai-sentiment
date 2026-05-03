from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .logic import analyze_sentiment

def sentiment_view(request):
    text = request.GET.get('text', '')
    result = analyze_sentiment(text)
    return JsonResponse(result)