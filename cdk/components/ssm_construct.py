from constructs import Construct
from aws_cdk import aws_s3 as s3, aws_ssm as ssm, aws_dynamodb as dynamodb


class SsmConstruct(Construct):
    
    ssm_tfstate_bucket_name_parameter: ssm.StringParameter
    
    def __init__(
        self, 
        scope: Construct, 
        construct_id: str, 
        state_bucket: s3.Bucket,
        lock_table: dynamodb.Table,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        self.ssm_tfstate_bucket_name_parameter = ssm.StringParameter(
            self,
            "TerraformStateBucketName",
            parameter_name=f"/tf-org-workspace/state-bucket-name",
            string_value=state_bucket.bucket_name,
            description="Bucket S3 para tfstate",
        )
        self.ssm_lock_table_name_parameter = ssm.StringParameter(
            self,
            "TerraformLockTableName",
            parameter_name=f"/tf-org-workspace/lock-table-name",
            string_value=lock_table.table_name,
            description="Tabela DynamoDB para lock do state",
        )