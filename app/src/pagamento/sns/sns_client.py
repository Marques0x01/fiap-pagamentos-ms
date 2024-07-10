class SnsClient:
    def __init__(self, sns_client) -> None:
        self.__sns_client = sns_client

    def send_message(self, message: str, subject: str, topic_arn: str):
        response = self.__sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject=subject
        )
        return response