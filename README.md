# terraform_bootstrap

Infraestrutura **AWS CDK em Python** (CloudFormation) que cria, **por conta/região**:

- **S3** com versionamento, criptografia gerenciada, bloqueio de acesso público e apenas TLS (`tf-org-workspace-state-<ACCOUNT_ID>`)
- **DynamoDB** on-demand com chave `LockID` para lock do state (`tf-org-workspace-locks-<ACCOUNT_ID>`)

Isso é o backend compartilhado para **outros repositórios Terraform**: cada projeto usa o mesmo bucket e tabela, com uma **`key`** distinta no S3 (ex.: `meu-app/prod/terraform.tfstate`).

O workflow em `.github/workflows/cd.yml` instala `requirements.txt`, roda `cdk bootstrap` (via `npx aws-cdk`) e `cdk deploy` nos pushes das branches `dev`, `homolog` e `prod`, mapeadas para secrets/vars de conta e região.

Local: `cd cdk && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && npx aws-cdk@2 synth` (exporte `AWS_ACCOUNT_ID` / `AWS_REGION` se quiser env explícito no stack ou adicione isso às variáveis do repositório).

Não precisa rodar isso a cada deploy de aplicação — só ao preparar conta/região ou mudar a política do backend.
