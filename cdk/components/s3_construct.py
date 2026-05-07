

from constructs import Construct
from aws_cdk import RemovalPolicy, Aws, aws_s3 as s3


class S3Construct(Construct):
    
    state_bucket: s3.Bucket
    
    def __init__(
        self, 
        scope: Construct, 
        construct_id: str, 
        **kwargs
    ) -> None:
        
        super().__init__(
            scope,
            construct_id,
            description="Construct para instanciar recursos s3",
            **kwargs,
        )
        
        account = Aws.ACCOUNT_ID

        self.state_bucket = s3.Bucket(
            self,
            "TerraformStateBucket",
            bucket_name=f"tf-org-workspace-state-{account}-{Aws.REGION}",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            removal_policy=RemovalPolicy.RETAIN,
    
        )