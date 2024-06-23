from datetime import datetime
from json import dumps


class PagseguroService:
    def __init__(self) -> None:
        pass

    def efetivar_pagamento_mock(self, id_cliente: str, valor_pagamento: str, id_beneficiario='FIAP Lanches') -> dict:
        return {'statusCode': 200, 'body': dumps({
                'nome': id_cliente,
                'beneficiario': id_beneficiario,
                'valor': valor_pagamento,
                'data_pagamento': datetime.now().isoformat(), 
                'message': 'Pagamento realizado com sucesso'
            })}
