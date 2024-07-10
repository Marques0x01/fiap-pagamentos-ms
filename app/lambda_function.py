import boto3
import json
from src.pagamento.dynamodb.repositories.dynamo_db_repository import DynamoDBRepository
from src.pagamento.dynamodb.services.dynamo_db_service import DynamoDBService
from src.pagamento.pagseguro.services.pagseguro_service import PagseguroService
from src.pagamento.sns.sns_client import SnsClient
from src.services.pagamento_service import PagamentoService
from src.services.estorno_service import EstornoService
from src.models.pagamento_model import PagamentoModel

try:
    table_name = 'fiap_pagamentos'
    AWS_REGION = 'us-east-2'
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    sns = boto3.client('sns', region_name=AWS_REGION)
    sns_client = SnsClient(sns_client=sns)
    dynamo_repository = DynamoDBRepository(table_name, dynamodb)
    dynamo_service = DynamoDBService(dynamo_repository)
    pagamento_service = PagamentoService(dynamo_service, PagseguroService(), sns_client)
    estorno_service = EstornoService(dynamo_service, sns_client)
except Exception as ex:
    raise ex

def lambda_handler(event, context):
    try:
        if event['httpMethod'] not in ['POST', 'PUT']:
            return {'statusCode': 405, 'body': json.dumps({'message': 'Method Not Allowed'})}

        data = json.loads(event['body'])
        pagamento = PagamentoModel(**data)
        
        if event['httpMethod'] == 'POST':
            response = pagamento_service.realizar_pagamento(pagamento)
        elif event['httpMethod'] == 'PUT':
            # Aqui você pode definir o comportamento para requisições PUT, se necessário.
            # Se o comportamento for o mesmo, pode chamar o mesmo método:
            pk = data['id_cliente']
            sk = data['id_pedido']
            motivo_estorno = data.get('motivo_estorno', 'falha no processamento')
            response = estorno_service.realizar_estorno(pk, sk, motivo_estorno)
        
        return {'statusCode': 200, 'body': json.dumps(response)}
    except ValueError:
        return {'statusCode': 400, 'body': json.dumps({'message': 'Invalid JSON'})}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'message': str(e)})}
