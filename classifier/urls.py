from django.urls import path
from .views import sentiment_view

urlpatterns = [
    path('analyze/', sentiment_view, name='analyze'),
]