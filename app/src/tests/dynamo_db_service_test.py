import unittest
from unittest.mock import MagicMock
from src.pagamento.dynamodb.repositories.dynamo_db_repository import DynamoDBRepository
from src.pagamento.dynamodb.services.dynamo_db_service import DynamoDBService

class TestDynamoDBService(unittest.TestCase):
    def setUp(self):
        self.repository = MagicMock(spec=DynamoDBRepository)
        self.service = DynamoDBService(self.repository)

    def test_add_item_success(self):
        item = {'key': 'value'}
        self.repository.put_item.return_value = (True, 'success')

        response = self.service.add_item(item)

        self.repository.put_item.assert_called_once_with(item)
        self.assertEqual(response, {'statusCode': 200, 'body': {'message': 'Item inserido com sucesso'}})

    def test_add_item_failure(self):
        item = {'key': 'value'}
        self.repository.put_item.return_value = (False, 'error')

        response = self.service.add_item(item)

        self.repository.put_item.assert_called_once_with(item)
        self.assertEqual(response, {'statusCode': 500, 'body': {'message': 'Erro ao inserir item na tabela: error'}})

if __name__ == '__main__':
    unittest.main()
