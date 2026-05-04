from django.urls import path
from .views import sentiment_view, debug_view

urlpatterns = [
    path('analyze/', sentiment_view, name='analyze'),
    path('debug/', debug_view, name='debug'),
]