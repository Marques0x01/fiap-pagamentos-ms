import logging
from src.pagamento.dynamodb.services.dynamo_db_service import DynamoDBService
from src.pagamento.sns.sns_client import SnsClient


class EstornoService:
    def __init__(self, dynamo_service: DynamoDBService, sns_client: SnsClient):
        """
        Inicializa uma nova instância de EstornoService.

        Args:
            dynamo_service (DynamoDBService): Serviço para interações com DynamoDB.
            sns_client (SnsClient): Cliente SNS para enviar notificações.
        """
        self.__dynamo_service = dynamo_service
        self.__notificacao_estorno = sns_client

    def realizar_estorno(self, pk: str, sk: str, motivo_estorno: str) -> dict:
        """
        Realiza um estorno.

        Args:
            pk (str): Chave primária do item.
            sk (str): Chave de classificação do item.
            motivo_estorno (str): Motivo do estorno.

        Returns:
            dict: O resultado do estorno.
        """
        try:
            update_expression = "set status_pagamento = :s, motivo_estorno = :m"
            expression_attribute_values = {
                ":s": "estornado",
                ":m": motivo_estorno
            }
            resultado_atualizacao = self.__dynamo_service.update_item(pk, sk, update_expression, expression_attribute_values)
            if 'Attributes' in resultado_atualizacao:
                self.__notificacao_estorno.send_message(
                    message=f"Estorno realizado com sucesso para o item com PK: {pk} e SK: {sk}",
                    subject="Estorno realizado com sucesso",
                    topic_arn="arn:aws:sns:us-east-2:767398154314:notificacao_pagamento"
                )
                return {'statusCode': 200, 'body': resultado_atualizacao['Attributes']}
            else:
                raise Exception("Erro ao atualizar o item no DynamoDB")
        except Exception as e:
            error_message = f"Erro ao processar o estorno: {str(e)}"
            logging.error(error_message, exc_info=True)
            self.__notificacao_estorno.send_message(
                message=error_message,
                subject="Erro ao processar o estorno",
                topic_arn="arn:aws:sns:us-east-2:767398154314:notificacao_pagamento"
            )
            return {'statusCode': 500, 'message': error_message}
