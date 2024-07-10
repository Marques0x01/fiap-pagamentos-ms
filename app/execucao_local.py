from lambda_function import lambda_handler
from uuid import uuid4
import json
id_massa = str(uuid4())
pedido = {
    'httpMethod': 'PUT',
    'body': json.dumps({"id_cliente": id_massa,"id_pedido": str(uuid4()),"tipo_pagamento": "tipo_pagamento","valor_pagamento": "valor_pagamento"})}

print(lambda_handler(pedido, None))