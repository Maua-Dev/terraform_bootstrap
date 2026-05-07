#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stack.tf_state_stack import TerraformStateBackendStack


def main() -> None:
    app = cdk.App()

    account = os.environ.get("AWS_ACCOUNT_ID") or os.environ.get("CDK_DEFAULT_ACCOUNT")
    region = os.environ.get("AWS_REGION") or os.environ.get("CDK_DEFAULT_REGION")

    env = cdk.Environment(account=account, region=region) if account and region else None

    TerraformStateBackendStack(app, "TerraformStateBackend", env=env)

    app.synth()


if __name__ == "__main__":
    main()
