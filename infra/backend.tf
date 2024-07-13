terraform {
  backend "s3" {
    bucket         = "backend-projeto"
    key            = "fiap_pagamentos_ms/terraform.tfstate"
    region         = "us-east-2"
    
  }
}
