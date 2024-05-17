class PagamentoModel:
    def __init__(self, id_cliente, id_pedido, tipo_pagamento, valor_pagamento):
        self.id_cliente = id_cliente
        self.id_pedido = id_pedido
        self.tipo_pagamento = tipo_pagamento
        self.valor_pagamento = valor_pagamento

    def to_dict(self):
        return {
            'pk': self.id_cliente,
            'sk': self.id_pedido,
            'tipo_pagamento': self.tipo_pagamento,
            'valor_pagamento': self.valor_pagamento,
        }