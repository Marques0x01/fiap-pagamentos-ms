from src.pagamento.dynamodb.services.dynamo_db_service import DynamoDBService
from src.pagamento.pagseguro.services.pagseguro_service import PagseguroService
from src.models.pagamento_model import PagamentoModel


class PagamentoService:
    def __init__(self, dynamo_service: DynamoDBService, pagseguro_service: PagseguroService) -> dict:
        self.__dynamo_service = dynamo_service
        self.__pagseguro_service = pagseguro_service

    def realizar_pagamento(self, pagamento_request: PagamentoModel):
        """
        Realiza um pagamento.

        Args:
            pagamento_request (PagamentoModel): O modelo de pagamento.

        Returns:
            dict: O resultado do pagamento.
        """
        response_pagseguro: dict = self.__pagseguro_service.efetivar_pagamento_mock(
                                        pagamento_request.id_cliente,
                                        pagamento_request.valor_pagamento)

        if response_pagseguro.get('statusCode') != 200:
            return response_pagseguro

        resultado_persistencia = self.__dynamo_service.add_item(pagamento_request.to_dict())

        if resultado_persistencia.get('statusCode') == 200:
            return response_pagseguro
        else:
            return resultado_persistencia

