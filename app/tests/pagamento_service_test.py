import unittest
from unittest.mock import MagicMock
from src.pagamento.dynamodb.services.dynamo_db_service import DynamoDBService
from src.pagamento.pagseguro.services.pagseguro_service import PagseguroService
from src.models.pagamento_model import PagamentoModel
from src.services.pagamento_service import PagamentoService

class TestPagamentoService(unittest.TestCase):
    def setUp(self):
        # Configuração dos mocks
        self.dynamo_service_mock = MagicMock(spec=DynamoDBService)
        self.pagseguro_service_mock = MagicMock(spec=PagseguroService)
        self.pagamento_service = PagamentoService(self.dynamo_service_mock, self.pagseguro_service_mock)

    def test_realizar_pagamento_com_sucesso(self):
        # Configuração dos mocks
        pagamento_request_mock = PagamentoModel(id_cliente='666', id_pedido='666', tipo_pagamento='PIQUIS', valor_pagamento='220')
        self.pagseguro_service_mock.efetivar_pagamento_mock.return_value = {'status': 200}
        self.dynamo_service_mock.add_item.return_value = {'statusCode': 200}

        # Chamada ao método realizar_pagamento
        resultado = self.pagamento_service.realizar_pagamento(pagamento_request_mock)

        # Verificações
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado, {'status': 200})

    def test_realizar_pagamento_com_falha_no_pagseguro(self):
        # Configuração dos mocks
        pagamento_request_mock = PagamentoModel(id_cliente='666', id_pedido='666', tipo_pagamento='PIQUIS', valor_pagamento='220')
        self.pagseguro_service_mock.efetivar_pagamento_mock.return_value = {'status': 400}

        # Chamada ao método realizar_pagamento
        resultado = self.pagamento_service.realizar_pagamento(pagamento_request_mock)

        # Verificações
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado, {'status': 400})

    def test_realizar_pagamento_com_falha_na_persistencia(self):
        # Configuração dos mocks
        pagamento_request_mock = PagamentoModel(id_cliente='666', id_pedido='666', tipo_pagamento='PIQUIS', valor_pagamento='220')
        self.pagseguro_service_mock.efetivar_pagamento_mock.return_value = {'status': 200}
        self.dynamo_service_mock.add_item.return_value = {'statusCode': 500}

        # Chamada ao método realizar_pagamento
        resultado = self.pagamento_service.realizar_pagamento(pagamento_request_mock)

        # Verificações
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado, {'statusCode': 500})

if __name__ == '__main__':
    unittest.main()
