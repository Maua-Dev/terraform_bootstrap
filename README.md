# terraform_bootstrap
Terraform na AWS: bucket S3 (state) + tabela DynamoDB (lock). Backend compartilhado entre projetos; cada stack usa um key distinto. Rodar ao abrir conta/região nova ou mudar política do backend. Não rodar a cada deploy de aplicação.
