import boto3

ENDPOINT_URL = 'http://localhost:4566'
REGION_AWS = 'us-east-2'
AWS_KEY = 'test'

'''
Criação da fila SQS "notificacao_pagamento"
'''
sqs = boto3.client(
    'sqs',
    endpoint_url=ENDPOINT_URL,  # Endpoint do LocalStack
    region_name=REGION_AWS,
    aws_access_key_id=AWS_KEY,
    aws_secret_access_key=AWS_KEY
)
# Criação da fila SQS
queue_name = 'notificacao_pagamento'
response = sqs.create_queue(QueueName=queue_name)
queue_url = response['QueueUrl']
print(f'Fila {queue_name} criada com URL: {queue_url}')

'''
Criação da tabela Dynamo "fiap_pagamentos"
'''

dynamodb = boto3.client(
    'dynamodb',
    endpoint_url=ENDPOINT_URL,  # Endpoint do LocalStack
    region_name=REGION_AWS,
    aws_access_key_id=AWS_KEY,
    aws_secret_access_key=AWS_KEY
)
# Criação da tabela DynamoDB com chave de partição e chave de classificação
table_name = 'fiap_pagamentos'
response = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
        {
            'AttributeName': 'pk',
            'KeyType': 'HASH'  # Chave de partição
        },
        {
            'AttributeName': 'sk',
            'KeyType': 'RANGE'  # Chave de classificação
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'pk',
            'AttributeType': 'S'  # Tipo de atributo (S = String)
        },
        {
            'AttributeName': 'sk',
            'AttributeType': 'S'  # Tipo de atributo (S = String)
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

print(f'Tabela {table_name} criada com descrição: {response["TableDescription"]}')
