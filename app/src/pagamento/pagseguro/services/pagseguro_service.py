from datetime import datetime


class PagseguroService:
    def __init__(self) -> None:
        pass

    def efetivar_pagamento_mock(self, id_cliente: str, valor_pagamento: str, id_beneficiario='FIAP Lanches') -> dict:
        return {
                'nome': id_cliente,
                'beneficiario': id_beneficiario,
                'valor': valor_pagamento,
                'data_pagamento': datetime.now(), 
                'status': 200, 
                'message': 'Pagamento realizado com sucesso'
            }