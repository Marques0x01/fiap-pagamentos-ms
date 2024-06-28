terraform {
  backend "s3" {
    bucket         = "backend-fiap-pos"
    key            = "fiap_pagamentos_ms/terraform.tfstate"
    region         = "us-east-1"
    
  }
}
