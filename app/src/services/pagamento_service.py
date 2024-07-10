from src.pagamento.dynamodb.services.dynamo_db_service import DynamoDBService
from src.pagamento.pagseguro.services.pagseguro_service import PagseguroService
from src.pagamento.sns.sns_client import SnsClient
from src.models.pagamento_model import PagamentoModel
import logging

class PagamentoService:
    def __init__(self, dynamo_service: DynamoDBService, pagseguro_service: PagseguroService, sns_client: SnsClient):
        """
        Inicializa uma nova instância de PagamentoService.

        Args:
            dynamo_service (DynamoDBService): Serviço para interações com DynamoDB.
            pagseguro_service (PagseguroService): Serviço para interações com PagSeguro.
            sns_client (SnsClient): Cliente SNS para enviar notificações.
        """
        self.__dynamo_service = dynamo_service
        self.__pagseguro_service = pagseguro_service
        self.__notificacao_pagamento = sns_client

    def realizar_pagamento(self, pagamento_request: PagamentoModel) -> dict:
        """
        Realiza um pagamento.

        Args:
            pagamento_request (PagamentoModel): O modelo de pagamento.

        Returns:
            dict: O resultado do pagamento.
        """
        try:
            # Efetuar pagamento usando o serviço PagSeguro
            response_pagseguro: dict = self.__pagseguro_service.efetivar_pagamento_mock(
                pagamento_request.id_cliente,
                pagamento_request.valor_pagamento
            )

            if response_pagseguro.get('statusCode') != 200:
                # Publicar mensagem de erro no SNS
                self.__notificacao_pagamento.send_message(
                    message=str(response_pagseguro),
                    subject='Ocorreu um problema ao efetivar o pagamento',
                    topic_arn='arn:aws:sns:us-east-2:767398154314:notificacao_pagamento'
                )
                return response_pagseguro

            # Persistir o pagamento no DynamoDB
            pagamento_data = pagamento_request.to_dict()
            pagamento_data['status_pagamento'] = 'efetivado'
            resultado_persistencia = self.__dynamo_service.add_item(pagamento_data)

            if resultado_persistencia.get('statusCode') == 200:
                # Publicar mensagem de sucesso no SNS
                self.__notificacao_pagamento.send_message(
                    message=str(pagamento_request.to_dict()),
                    subject='Pagamento realizado com sucesso',
                    topic_arn='arn:aws:sns:us-east-2:767398154314:notificacao_pagamento'
                )
                return response_pagseguro
            else:
                # Publicar mensagem de erro no SNS
                self.__notificacao_pagamento.send_message(
                    message=str(resultado_persistencia),
                    subject='Erro ao persistir dados do pagamento',
                    topic_arn='arn:aws:sns:us-east-2:767398154314:notificacao_pagamento'
                )
                return resultado_persistencia

        except Exception as e:
            error_message = f"Erro ao processar o pagamento: {str(e)}"
            logging.error(error_message, exc_info=True)
            # Publicar mensagem de exceção no SNS
            self.__notificacao_pagamento.send_message(
                message=error_message,
                subject='Erro ao processar o pagamento',
                topic_arn='arn:aws:sns:us-east-2:767398154314:notificacao_pagamento'
            )
            return {'statusCode': 500, 'message': error_message}
