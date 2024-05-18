Feature: Realizar Pagamento

  Scenario: Pagamento com sucesso
    Given um pagamento com ID do cliente "jamal" e valor de pagamento "70.00"
    And o serviço de PagSeguro está funcionando corretamente
    And o serviço DynamoDB está funcionando corretamente
    When o pagamento é realizado
    Then o pagamento é efetuado com sucesso

  Scenario: Falha na Persistência
    Given um pagamento com ID do cliente "jamal" e valor de pagamento "70.00"
    And o serviço de PagSeguro está funcionando corretamente
    And o serviço DynamoDB está com falha
    When o pagamento é realizado
    Then a persistência do pagamento falha
