Feature: Análisis de Sentimiento
  Scenario: Clasificar un texto simple
    Given que el servicio está listo
    When envío el texto "Estoy muy feliz"
    Then el resultado debe ser "positivo"