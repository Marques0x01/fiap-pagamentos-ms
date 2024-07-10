from src.pagamento.dynamodb.repositories.dynamo_db_repository import DynamoDBRepository
from json import dumps
class DynamoDBService:
    def __init__(self, dynamo_repository: DynamoDBRepository):
        self.__repository = dynamo_repository

    def add_item(self, item: dict):
        success, response = self.__repository.put_item(item)
        if success:
            return {'statusCode': 200, 'body': dumps({'message': 'Item inserido com sucesso'})}
        else:
            return {'statusCode': 500, 'body': dumps({'message': f'Erro ao inserir item na tabela: {response}'})}
        
    def update_item(self, pk, sk, update_expression, expression_attribute_values):
        return self.__repository.update_item(pk, sk, update_expression, expression_attribute_values)
