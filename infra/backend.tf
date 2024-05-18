terraform {
  backend "s3" {
    bucket         = "fiap-tfstates"
    key            = "fiap_pagamentos_ms/terraform.tfstate"
    region         = "us-east-1"
    
  }
}
