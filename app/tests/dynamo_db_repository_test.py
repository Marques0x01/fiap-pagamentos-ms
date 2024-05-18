import unittest
from unittest.mock import MagicMock
from app.src.pagamento.dynamodb.repositories.dynamo_db_repository import DynamoDBRepository

class TestDynamoDBRepository(unittest.TestCase):
    def test_put_item_sucesso(self):
        # Mock do recurso DynamoDB
        dynamodb_resource_mock = MagicMock()
        table_mock = MagicMock()
        dynamodb_resource_mock.Table.return_value = table_mock

        # Criando uma instância da classe com o mock do recurso DynamoDB
        dynamodb_repository = DynamoDBRepository("nome_da_tabela", dynamodb_resource_mock)

        # Chamando o método put_item com um item mockado
        item_mock = {"chave": "valor"}
        result, response = dynamodb_repository.put_item(item_mock)

        # Verificando se o método put_item da tabela foi chamado corretamente com os argumentos esperados
        table_mock.put_item.assert_called_once_with(Item=item_mock)

        # Verificando o resultado
        self.assertTrue(result)
    
    def test_put_item_falha(self):
        # Mock do recurso DynamoDB
        dynamodb_resource_mock = MagicMock()
        table_mock = MagicMock()
        dynamodb_resource_mock.Table.return_value = table_mock

        # Criando uma instância da classe com o mock do recurso DynamoDB
        dynamodb_repository = DynamoDBRepository("nome_da_tabela", dynamodb_resource_mock)

        # Configurando o mock para simular uma exceção ao chamar put_item
        table_mock.put_item.side_effect = Exception("Erro ao inserir item")

        # Chamando o método put_item com um item mockado
        item_mock = {"chave": "valor"}
        result, response = dynamodb_repository.put_item(item_mock)

        # Verificando se o método put_item da tabela foi chamado corretamente com os argumentos esperados
        table_mock.put_item.assert_called_once_with(Item=item_mock)

        # Verificando o resultado
        self.assertFalse(result)
        self.assertEqual(response, "Erro ao inserir item")

if __name__ == '__main__':
    unittest.main()
