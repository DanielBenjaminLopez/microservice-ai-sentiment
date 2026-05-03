from behave import given, when, then
from classifier.logic import analyze_sentiment

@given('que el servicio está listo')
def step_impl(context):
    pass  # Por ahora no requiere preparación técnica

@when('envío el texto "{text}"')
def step_impl(context, text):
    context.result = analyze_sentiment(text)

@then('el resultado debe ser "{expected_label}"')
def step_impl(context, expected_label):
    assert context.result['label'] == expected_label