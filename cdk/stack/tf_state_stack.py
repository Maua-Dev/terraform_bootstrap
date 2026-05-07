from constructs import Construct
from aws_cdk import Stack
from components.s3_construct import S3Construct
from components.dynamo_construct import DynamoConstruct
from aws_cdk import CfnOutput

class TerraformStateBackendStack(Stack):
    
    def __init__(
        self, 
        scope: Construct, 
        stack_id: str, 
        **kwargs
    ) -> None:
        
        super().__init__(
            scope,
            stack_id,
            description="S3 + DynamoDB para estado remoto e lock do Terraform.",
            **kwargs,
        )
        
        s3_construct = S3Construct(self, "S3Construct")
        dynamo_construct = DynamoConstruct(self, "DynamoConstruct")
        
        CfnOutput(
            self,
            "StateBucketName",
            value=s3_construct.state_bucket.bucket_name,
            description="Bucket S3 para tfstate (use no backend Terraform)",
        )
        CfnOutput(
            self,
            "LockTableName",
            value=dynamo_construct.lock_table.table_name,
            description="Tabela DynamoDB para lock do state",
        )
        CfnOutput(
            self,
            "AwsRegion",
            value=self.region,
            description="Região do backend",
        )

        
    