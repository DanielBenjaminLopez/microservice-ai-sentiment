import pytest
from classifier.logic import analyze_sentiment

def test_sentiment_analysis_basic():
    """Prueba que la lógica devuelva una estructura válida"""
    result = analyze_sentiment("Estoy muy feliz")
    assert "label" in result
    assert result["label"] in ["positivo", "negativo", "neutral"]