import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = current_dir.replace(os.path.join('tests', 'automated', 'steps'), '')
sys.path.append(src_dir)
from behave import given, when, then
from unittest.mock import MagicMock
from src.pagamento.dynamodb.services.dynamo_db_service import DynamoDBService
from src.pagamento.pagseguro.services.pagseguro_service import PagseguroService
from src.models.pagamento_model import PagamentoModel
from src.services.pagamento_service import PagamentoService

@given('um pagamento com ID do cliente "{cliente}" e valor de pagamento "{valor}"')
def step_given_pagamento(context, cliente, valor):
    context.pagamento_request = PagamentoModel(
        id_cliente=cliente,
        valor_pagamento=float(valor),
        tipo_pagamento="PIX",
        id_pedido="toma"
    )
    print("Step: Given um pagamento")

@given('o serviço de PagSeguro está funcionando corretamente')
def step_given_pagseguro_service(context):
    context.pagseguro_service_mock = MagicMock(spec=PagseguroService)
    context.pagseguro_service_mock.efetivar_pagamento_mock.return_value = {'status': 200}
    print("Step: Given o serviço de PagSeguro está funcionando corretamente")

@given('o serviço DynamoDB está funcionando corretamente')
def step_given_dynamodb_service(context):
    context.dynamo_service_mock = MagicMock(spec=DynamoDBService)
    context.dynamo_service_mock.add_item.return_value = {'statusCode': 200}
    print("Step: Given o serviço DynamoDB está funcionando corretamente")

@given('o serviço DynamoDB está com falha')
def step_given_dynamodb_service_failure(context):
    context.dynamo_service_mock = MagicMock(spec=DynamoDBService)
    context.dynamo_service_mock.add_item.return_value = {'statusCode': 500}
    print("Step: Given o serviço DynamoDB está com falha")

@when('o pagamento é realizado')
def step_when_pagamento_realizado(context):
    pagamento_service = PagamentoService(context.dynamo_service_mock, context.pagseguro_service_mock)
    context.resultado = pagamento_service.realizar_pagamento(context.pagamento_request)
    print("Step: When o pagamento é realizado")

@then('o pagamento é efetuado com sucesso')
def step_then_pagamento_sucesso(context):
    assert context.resultado == {'status': 200}
    print("Step: Then o pagamento é efetuado com sucesso")

@then('a persistência do pagamento falha')
def step_then_persistencia_falha(context):
    assert context.resultado == {'statusCode': 500}
    print("Step: Then a persistência do pagamento falha")
