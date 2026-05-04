"""
Behave environment hooks para mocking de la API de Gemini en tests.
"""
from unittest.mock import Mock
import classifier.logic as logic_module


def before_scenario(context, scenario):
    """
    Hook que se ejecuta antes de cada escenario.
    Prepara un modelo mockeado para no depender de API keys reales.
    """
    # Guardamos el modelo original para restaurarlo después
    context.original_model = logic_module.model
    
    # Creamos un modelo mockeado
    mock_model = Mock()
    logic_module.model = mock_model
    
    # Configuramos respuestas por defecto según el texto de entrada
    def mock_generate_content(prompt, generation_config=None):
        mock_response = Mock()
        # Lógica simple para determinar sentimiento según palabras clave en el prompt
        if "feliz" in prompt.lower() or "bueno" in prompt.lower():
            mock_response.text = "positive"
        elif "triste" in prompt.lower() or "malo" in prompt.lower() or "problema" in prompt.lower():
            mock_response.text = "negative"
        else:
            mock_response.text = "neutral"
        return mock_response
    
    mock_model.generate_content.side_effect = mock_generate_content
    
    # Guardamos el mock en context para acceso desde los steps si es necesario
    context.mock_model = mock_model


def after_scenario(context, scenario):
    """
    Hook que se ejecuta después de cada escenario.
    Restaura el modelo original.
    """
    if hasattr(context, 'original_model'):
        logic_module.model = context.original_model
