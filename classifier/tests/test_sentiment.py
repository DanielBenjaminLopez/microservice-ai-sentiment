import pytest
import os
from unittest.mock import Mock
import classifier.logic as logic_module


@pytest.fixture
def mock_model(monkeypatch):
    """Fixture para proporcionar un modelo mockeado"""
    mock_model = Mock()
    monkeypatch.setattr(logic_module, 'model', mock_model)
    return mock_model


def test_sentiment_analysis_positive(mock_model):
    """Prueba con sentimiento positivo"""
    mock_response = Mock()
    mock_response.text = "positivo"
    mock_model.generate_content.return_value = mock_response
    
    result = logic_module.analyze_sentiment("Estoy muy feliz")
    assert result["label"] == "positivo"
    mock_model.generate_content.assert_called_once()


def test_sentiment_analysis_negative(mock_model):
    """Prueba con sentimiento negativo"""
    mock_response = Mock()
    mock_response.text = "negativo"
    mock_model.generate_content.return_value = mock_response
    
    result = logic_module.analyze_sentiment("Estoy triste")
    assert result["label"] == "negativo"


def test_sentiment_analysis_neutral(mock_model):
    """Prueba con sentimiento neutral"""
    mock_response = Mock()
    mock_response.text = "neutral"
    mock_model.generate_content.return_value = mock_response
    
    result = logic_module.analyze_sentiment("Hace buen tiempo")
    assert result["label"] == "neutral"


def test_sentiment_analysis_with_whitespace(mock_model):
    """Prueba que el texto se normaliza (strip y lower)"""
    mock_response = Mock()
    mock_response.text = "  POSITIVO  \n"
    mock_model.generate_content.return_value = mock_response
    
    result = logic_module.analyze_sentiment("Texto cualquiera")
    assert result["label"] == "positivo"


def test_sentiment_analysis_invalid_response(mock_model):
    """Prueba con respuesta inválida del modelo"""
    mock_response = Mock()
    mock_response.text = "invalid_sentiment"
    mock_model.generate_content.return_value = mock_response
    
    result = logic_module.analyze_sentiment("Texto")
    assert result["label"] == "neutral"


def test_sentiment_analysis_no_model(monkeypatch):
    """Prueba cuando no hay modelo disponible"""
    monkeypatch.setattr(logic_module, 'model', None)
    result = logic_module.analyze_sentiment("Estoy feliz")
    assert result == {"label": "neutral"}


def test_sentiment_analysis_empty_text(mock_model):
    """Prueba con texto vacío"""
    result = logic_module.analyze_sentiment("")
    assert result == {"label": "neutral"}
    mock_model.generate_content.assert_not_called()


def test_sentiment_analysis_exception(mock_model):
    """Prueba cuando la API lanza una excepción"""
    mock_model.generate_content.side_effect = Exception("API error")
    
    result = logic_module.analyze_sentiment("Texto")
    assert result == {"label": "neutral"}