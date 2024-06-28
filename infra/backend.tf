terraform {
  backend "s3" {
    bucket         = "tfstates-fiap-lanches"
    key            = "fiap_pagamentos_ms/terraform.tfstate"
    region         = "us-east-2"
    
  }
}
