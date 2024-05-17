terraform {
  backend "s3" {
    bucket         = "fiap-tfstates"
    key            = "fiap_pedidos_ms/terraform.tfstate"
    region         = "us-east-1"
    
  }
}
