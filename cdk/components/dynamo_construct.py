from aws_cdk import RemovalPolicy, aws_dynamodb as dynamodb
from aws_cdk import Aws
from constructs import Construct

class DynamoConstruct(Construct):
    
    lock_table: dynamodb.Table
    
    def __init__(
        self, 
        scope: Construct, 
        construct_id: str, 
        **kwargs
    ) -> None:
        
        super().__init__(scope, construct_id, **kwargs)
        
        account = Aws.ACCOUNT_ID
        
        self.lock_table = dynamodb.Table(
            self,
            "TerraformLocks",
            table_name=f"tf-org-workspace-locks-{account}",
            partition_key=dynamodb.Attribute(
                name="LockID", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN,
        )