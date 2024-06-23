terraform {
  backend "s3" {
    bucket         = "fiap-backend"
    key            = "fiap_pagamentos_ms/terraform.tfstate"
    region         = "us-east-1"
    
  }
}
