Feature: Análisis de Sentimiento
  Scenario: Clasificar un texto positivo
    Given que el servicio está listo
    When envío el texto "Estoy muy feliz"
    Then el resultado debe ser "positivo"

  Scenario: Clasificar un texto negativo
    Given que el servicio está listo
    When envío el texto "Estoy muy triste"
    Then el resultado debe ser "negativo"

  Scenario: Clasificar un texto neutral
    Given que el servicio está listo
    When envío el texto "El cielo es azul"
    Then el resultado debe ser "neutral"