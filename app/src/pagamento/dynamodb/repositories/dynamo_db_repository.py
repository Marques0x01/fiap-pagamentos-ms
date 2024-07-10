class DynamoDBRepository:
    def __init__(self, table_name: str, dynamodb_resource):
        self.__dynamodb = dynamodb_resource
        self.__table = self.__dynamodb.Table(table_name)

    def put_item(self, item):
        try:
            response = self.__table.put_item(Item=item)
            return True, response
        except Exception as e:
            return False, str(e)

    def update_item(self, pk, sk, update_expression, expression_attribute_values):
        response = self.__table.update_item(
            Key={'pk': pk, 'sk': sk},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return response
