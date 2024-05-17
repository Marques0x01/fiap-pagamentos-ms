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