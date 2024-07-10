import unittest
from unittest.mock import MagicMock, patch
from src.pagamento.dynamodb.services.dynamo_db_service import DynamoDBService
from src.pagamento.sns.sns_client import SnsClient
from src.services.estorno_service import EstornoService

class TestEstornoService(unittest.TestCase):
    
    def setUp(self):
        self.dynamo_service = MagicMock(DynamoDBService)
        self.sns_client = MagicMock(SnsClient)
        self.estorno_service = EstornoService(self.dynamo_service, self.sns_client)
    
    def test_realizar_estorno_success(self):
        # Mock the DynamoDB service update_item method
        self.dynamo_service.update_item.return_value = {
            'Attributes': {
                'status_pagamento': 'estornado',
                'motivo_estorno': 'Motivo de Teste'
            }
        }
        
        response = self.estorno_service.realizar_estorno('pk_test', 'sk_test', 'Motivo de Teste')
        
        self.dynamo_service.update_item.assert_called_once_with(
            'pk_test', 
            'sk_test', 
            'set status_pagamento = :s, motivo_estorno = :m', 
            {':s': 'estornado', ':m': 'Motivo de Teste'}
        )
        self.sns_client.send_message.assert_called_once()
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('body', response)
    
    def test_realizar_estorno_dynamodb_failure(self):
        # Mock the DynamoDB service update_item method to return no attributes
        self.dynamo_service.update_item.return_value = {}
        
        response = self.estorno_service.realizar_estorno('pk_test', 'sk_test', 'Motivo de Teste')
        
        self.dynamo_service.update_item.assert_called_once_with(
            'pk_test', 
            'sk_test', 
            'set status_pagamento = :s, motivo_estorno = :m', 
            {':s': 'estornado', ':m': 'Motivo de Teste'}
        )
        self.sns_client.send_message.assert_called_once()
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('message', response)
    
    @patch('logging.error')
    def test_realizar_estorno_exception(self, mock_logging_error):
        # Mock the DynamoDB service update_item method to raise an exception
        self.dynamo_service.update_item.side_effect = Exception("Test Exception")
        
        response = self.estorno_service.realizar_estorno('pk_test', 'sk_test', 'Motivo de Teste')
        
        self.dynamo_service.update_item.assert_called_once_with(
            'pk_test', 
            'sk_test', 
            'set status_pagamento = :s, motivo_estorno = :m', 
            {':s': 'estornado', ':m': 'Motivo de Teste'}
        )
        self.sns_client.send_message.assert_called_once()
        mock_logging_error.assert_called_once()
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('message', response)

if __name__ == '__main__':
    unittest.main()
