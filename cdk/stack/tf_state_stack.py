from constructs import Construct
from aws_cdk import Stack
from components.s3_construct import S3Construct
from components.dynamo_construct import DynamoConstruct
from components.ssm_construct import SsmConstruct
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
        
        s3_construct = S3Construct(self, "S3")
        dynamo_construct = DynamoConstruct(self, "Dynamo")
        ssm_construct = SsmConstruct(self, "SSM", state_bucket=s3_construct.state_bucket, lock_table=dynamo_construct.lock_table)