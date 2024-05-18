import boto3
import json
from src.pagamento.dynamodb.repositories.dynamo_db_repository import DynamoDBRepository
from src.pagamento.dynamodb.services.dynamo_db_service import DynamoDBService
from src.pagamento.pagseguro.services.pagseguro_service import PagseguroService
from src.services.pagamento_service import PagamentoService
from src.models.pagamento_model import PagamentoModel

try:
    table_name = 'fiap_pagamentos'
    dynamo_repository = DynamoDBRepository(table_name, boto3.resource('dynamodb', region_name='us-east-1'))
    dynamo_service = DynamoDBService(dynamo_repository)
    pagamento_service = PagamentoService(dynamo_service, PagseguroService())
except Exception as ex:
    raise ex

def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
        pagamento = PagamentoModel(**data)
        return pagamento_service.realizar_pagamento(pagamento)
    except ValueError:
        return {'statusCode': 400, 'body': json.dumps({'message': 'Invalid JSON'})}
