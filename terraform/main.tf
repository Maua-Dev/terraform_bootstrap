terraform {
  backend "s3" {
    encrypt = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "aws_account_id" {
  description = "ID da conta AWS (12 dígitos). Usado nos nomes globais do S3 e da tabela."
  type        = string

  validation {
    condition     = can(regex("^[0-9]{12}$", var.aws_account_id))
    error_message = "aws_account_id deve ter exatamente 12 dígitos."
  }
}

variable "aws_region" {
  description = "Região AWS do provider e do backend S3."
  type        = string
}

locals {
  workspace_state_bucket = "tf-org-workspace-state-${var.aws_account_id}"
  workspace_lock_table   = "tf-org-workspace-locks-${var.aws_account_id}"
}

provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "terraform_state" {
  bucket = local.workspace_state_bucket

  lifecycle {
    prevent_destroy = true

    precondition {
      condition     = data.aws_caller_identity.current.account_id == var.aws_account_id
      error_message = "Credenciais AWS são de outra conta: ajuste aws_account_id ou o OIDC/role do workflow."
    }
  }
}

resource "aws_s3_bucket_versioning" "versioning_example" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "block_public" {
  bucket                  = aws_s3_bucket.terraform_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = local.workspace_lock_table
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}

output "s3_bucket_name" {
  description = "Bucket S3 para estado Terraform de outros stacks nesta conta."
  value       = aws_s3_bucket.terraform_state.id
}

output "dynamodb_table_name" {
  description = "Tabela DynamoDB de lock para esse backend de workspace."
  value       = aws_dynamodb_table.terraform_locks.name
}

output "bootstrap_state_hint" {
  description = "Lembrete: o state deste módulo fica no bucket/tabela passados no terraform init -backend-config (não nos outputs acima)."
  value       = "Ver comentário no topo de main.tf"
}
