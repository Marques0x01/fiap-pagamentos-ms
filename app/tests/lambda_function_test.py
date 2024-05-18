import unittest
from unittest.mock import MagicMock
from lambda_function import lambda_handler

class TestLambdaHandler(unittest.TestCase):
    def setUp(self):
        # Configuração dos mocks
        self.dynamo_service_mock = MagicMock()
        self.pagseguro_service_mock = MagicMock()

    def test_lambda_handler_com_json_valido_erro_ao_persistir_dado(self):
        # Configuração dos mocks
        event = {'body': '{"id_cliente":"jamal","valor_pagamento":"70.00","id_pedido":"666","tipo_pagamento":"PIX"}'}
        context = MagicMock()

        # Chamada ao lambda_handler com mocks passados como argumentos
        resultado = lambda_handler(event, context)

        # Verificações
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['statusCode'], 500)

    def test_lambda_handler_com_json_invalido(self):
        # Configuração dos mocks
        event = {'body': 'invalid_json'}
        context = MagicMock()

        # Chamada ao lambda_handler com mocks passados como argumentos
        resultado = lambda_handler(event, context)

        # Verificações
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['statusCode'], 400)

if __name__ == '__main__':
    unittest.main()
