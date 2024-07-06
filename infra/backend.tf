terraform {
  backend "s3" {
    bucket         = "backend-fiap"
    key            = "fiap_pagamentos_ms/terraform.tfstate"
    region         = "us-east-2"
    
  }
}
