variable "lambda_name" {
  description = "Lambda name"
  type        = string
}

variable "policies_name" {
  description = "Policy name"
  type        = string
  default     = "t2.micro"
}

variable "role_name" {
  description = "Role name"
  type        = string
}

variable "bucket_backend_name" {
  description = "Bucket backend name"
  type        = string
}

variable "region" {
  description = "Region name"
  type        = string
  default     = "us-east-2"
}

variable "env_vars" {
  description = "Enviroment variables"
  type        = object({})
  default     = {}
}

