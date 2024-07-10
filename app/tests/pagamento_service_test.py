import unittest
from unittest.mock import Mock, patch
from src.pagamento.dynamodb.services.dynamo_db_service import DynamoDBService
from src.pagamento.pagseguro.services.pagseguro_service import PagseguroService
from src.pagamento.sns.sns_client import SnsClient
from src.models.pagamento_model import PagamentoModel
# from src.pagamento.services.pagamento_service import PagamentoService
from src.services.pagamento_service import PagamentoService

class TestPagamentoService(unittest.TestCase):

    @patch('src.pagamento.dynamodb.services.dynamo_db_service.DynamoDBService')
    @patch('src.pagamento.pagseguro.services.pagseguro_service.PagseguroService')
    @patch('src.pagamento.sns.sns_client.SnsClient')
    def setUp(self, MockDynamoDBService, MockPagseguroService, MockSnsClient):
        self.dynamo_service = MockDynamoDBService()
        self.pagseguro_service = MockPagseguroService()
        self.sns_client = MockSnsClient()
        self.pagamento_service = PagamentoService(self.dynamo_service, self.pagseguro_service, self.sns_client)

    def test_realizar_pagamento_sucesso(self):
        # Mock response for successful PagSeguro payment
        self.pagseguro_service.efetivar_pagamento_mock.return_value = {'statusCode': 200}
        # Mock response for successful DynamoDB persistence
        self.dynamo_service.add_item.return_value = {'statusCode': 200}

        pagamento_request = PagamentoModel(id_cliente='123', valor_pagamento=100.00, tipo_pagamento='PIX', id_pedido='666')

        response = self.pagamento_service.realizar_pagamento(pagamento_request)

        self.assertEqual(response['statusCode'], 200)
        self.sns_client.send_message.assert_called_with(
            message=str(pagamento_request.to_dict()),
            subject='Pagamento realizado com sucesso',
            topic_arn='arn:aws:sns:us-east-2:767398154314:notificacao_pagamento'
        )

    def test_realizar_pagamento_falha_pagseguro(self):
        # Mock response for failed PagSeguro payment
        self.pagseguro_service.efetivar_pagamento_mock.return_value = {'statusCode': 500}

        pagamento_request = PagamentoModel(id_cliente='123', valor_pagamento=100.00, id_pedido='666', tipo_pagamento='Agiotagem')

        response = self.pagamento_service.realizar_pagamento(pagamento_request)

        self.assertEqual(response['statusCode'], 500)
        self.sns_client.send_message.assert_called_with(
            message=str({'statusCode': 500}),
            subject='Ocorreu um problema ao efetivar o pagamento',
            topic_arn='arn:aws:sns:us-east-2:767398154314:notificacao_pagamento'
        )

    def test_realizar_pagamento_falha_persistencia(self):
        # Mock response for successful PagSeguro payment
        self.pagseguro_service.efetivar_pagamento_mock.return_value = {'statusCode': 200}
        # Mock response for failed DynamoDB persistence
        self.dynamo_service.add_item.return_value = {'statusCode': 500}

        pagamento_request = PagamentoModel(id_cliente='123', valor_pagamento=100.00, tipo_pagamento='TED', id_pedido='666')

        response = self.pagamento_service.realizar_pagamento(pagamento_request)

        self.assertEqual(response['statusCode'], 500)
        self.sns_client.send_message.assert_called_with(
            message=str({'statusCode': 500}),
            subject='Erro ao persistir dados do pagamento',
            topic_arn='arn:aws:sns:us-east-2:767398154314:notificacao_pagamento'
        )

    def test_realizar_pagamento_excecao(self):
        # Mock PagSeguro to raise an exception
        self.pagseguro_service.efetivar_pagamento_mock.side_effect = Exception('Erro no PagSeguro')

        pagamento_request = PagamentoModel(id_cliente='123', valor_pagamento=100.00, id_pedido='666', tipo_pagamento='Cheque')

        response = self.pagamento_service.realizar_pagamento(pagamento_request)

        self.assertEqual(response['statusCode'], 500)
        self.sns_client.send_message.assert_called_with(
            message='Erro ao processar o pagamento: Erro no PagSeguro',
            subject='Erro ao processar o pagamento',
            topic_arn='arn:aws:sns:us-east-2:767398154314:notificacao_pagamento'
        )

if __name__ == '__main__':
    unittest.main()
