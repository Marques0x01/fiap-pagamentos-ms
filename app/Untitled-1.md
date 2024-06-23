https://github.com/Marques0x01/fiap_rds_infra
https://github.com/Marques0x01/fiap-lanches
https://github.com/Marques0x01/fiap-lanches-helm
https://github.com/Marques0x01/fiap_eks_cluster
https://github.com/Marques0x01/fiap_api_gateway
https://github.com/Marques0x01/fiap_lambda_auth

helm define os seguintes itens
explicação do helm
imagem ECR
cria load balancer
Configura os secrets do cluster EKS


API gateway
    configuração de permissão do gateway para acessar o lambda

Lambda
    tem 3 endpoints 
        create
        login
        confirmation
    todo acessam o cognito para realizar a autenticação


https://github.com/Marques0x01/fiap_eks_cluster
https://github.com/Marques0x01/fiap-lanches-helm
https://github.com/Marques0x01/fiap-lanches
https://github.com/Marques0x01/fiap_rds_infra
https://github.com/Marques0x01/fiap_api_gateway
https://github.com/Marques0x01/fiap_lambda_auth

# comando para executar os testes + cobertura
coverage run -m unittest discover -s tests -p "*_test.py"
coverage xml -o coverage-reports/coverage.xml
