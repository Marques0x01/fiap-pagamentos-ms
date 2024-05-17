from src.pagamento.dynamodb.repositories.dynamo_db_repository import DynamoDBRepository
from json import dumps
class DynamoDBService:
    def __init__(self, dynamo_repository: DynamoDBRepository):
        self.__repository = dynamo_repository

    def add_item(self, item: dict):
        success, response = self.__repository.put_item(item)
        if success:
            return {'statusCode': 200, 'body': {'message': 'Item inserido com sucesso'}}
        else:
            return {'statusCode': 500, 'body': {'message': f'Erro ao inserir item na tabela: {response}'}}
