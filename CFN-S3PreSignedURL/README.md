## Transfer Files to S3 Using REST API
### Goal
Invoke a PowerShell script which refers to a REST API to transfer files.
### Objectives
To create an AWS stack which creates the necessary infractructure to:
- issue pre-signed URLs for read and write operations into an S3 bucket
- notify subscribers of the SNS notification topic of requested operation


To use the PowerShell script to transfer the file to and from S3.

### Contents
- **APIGateway.yaml** REST API CloudFormation Template
- **IAM.yaml** Policies and Roles CloudFormation Template
- **Lambda.yaml** Lambda Function and Layer CloudFormation Template
- **Lambda<>.py** Execution code in Python
- **S3.yaml** Bucket and Life Cycle Policy CloudFormation Template
- **SNS.yaml** Notification Topic, Policy and Subscription CloudFormation Template
- **Start.yaml** Root CloudFormation Stack - use this to create the stack.
- **Transfer-Files.ps1** PowerShell script used to transfer files between local computer and S3 bucket.

### Deployment
#### Prepare the S3 bucket hosting the code
Create a bucket in the region where you plan to deploy the infrastructure.
Create the following structure in the bucket using the files in this folder:
```
s3://mycodebucket
.
+-- APIGateway.yaml
+-- Iam.yaml
+-- Lambda.yaml
+-- Lambda
|   +-- Functions
|   |   +-- LambdaCreateS3PreSignedURL.zip
|   +-- LambdaExceptions.zip
+-- README.md (optional)
+-- S3.yaml
+-- SNS.yaml
+-- Start.yaml

where the zip files are created as follows:

LambdaCreateS3PreSignedURL.zip
.
+-- LambdaCreateS3PreSignedURL.py

LambdaExceptions.zip
.
+-- python
    +-- LambdaExceptions.py
```
#### Create the CloudFormation stack
Use the `S3 Object URL` to Start.yaml to create the stack.
|Parameter|Value|Remarks|
|-|-|-|
|ContactEmail|*Your e-mail goes here*|Do not forget to confirm subscription. Other e-mails can be added manually.|
|CostCenter|*Billing Tag*|For the tracking of costs. This is used extensively in the CFN code for creating unique names.|
|Name|*your project name*|Can be the same as the stack name|
|S3CFNURL|*S3 bucket URL*|This is used by CFN to refer to the nested stacks. For example: `https://s3-eu-west-1.amazonaws.com/mycodebucket`|
|S3CodeBucket|*Name of the S3 bucket hosting the lambda code*|In this case, this is the same bucket created at the previous step. For example, `mycodebucket`|

Make note of the Outputs from some of the nested stacks. Specifically,
|Stack|Parameter|Value|Remarks|
|-|-|-|-|
|APIGateway|CostCenterRESTAPIDevEndpointUrl|`https://<REST API Id>.execute-api.<AWS Region>.amazonaws.com/dev`|URL for development stage.|
|APIGateway|CostCenterRESTAPIProdEndpointUrl|`https://<REST API Id>.execute-api.<AWS Region>.amazonaws.com/prod`|URL for production stage. Required in the PowerShell script.|
|Lambda|LambdaCreateS3PreSignedURLArn|`arn:aws:lambda:<AWs Region>:<AWS Account No>:function:LambdaCreateS3PreSignedURL-<CostCenter>`|This is the unqualified Arn, which is used to configure the API for Lambda invokation.|
|SNS|SNSNotifyMeArn|`arn:aws:sns:eu-west-1:<AWS Account No>:SNS-Email-my-account-<CostCenter>`|Required for handling subscriptions to the topic.|
|S3|S3StagingAreaBucket|`staging.area.<CostCenter>`|Required to know where to store objects in S3. Note the 14 day LifeCycle policy attached to the bucket.|

#### Allow the API to invoke Lambda
The REST API needs to have permissions to invoke the Lambda function.
This is done for both the development and production stages. This implementation decouples the development from production completely.
The standard AWS CLI command to run is (on Linux):


`aws lambda add-permission \`


`--function-name "<LambdaCreateS3PreSignedURLArn>:${stageVariables.lambdaAlias}" \`


`--source-arn "arn:aws:execute-api:<AWS Region>:<AWS Account No>:<REST API Id>:<Deployment Stage>/GET/access" \`


`--principal apigateway.amazonaws.com \`


`--statement-id 12345678-1234-1234-1234-123456789012 \`


`--action lambda:InvokeFunction`


Replace "\" with "^" to run the same command on Windows.
Make the following substitutions:
|`${stageVariables.lambdaAlias}`|`<Deployment Stage>`|
|-|-|
|dev|DEVEL|
|prod|PROD|


The `statement-id` needs to be unique for each command.

#### Prepare the PowerShell Script
Open the Transfer-File.ps1 and change this line to be applicable to your implementation (CostCenterRESTAPIProdEndpointUrl):


`$uri = "https://<REST-API-Id>.execute-api.<AWS Region>.amazonaws.com/<Deployment stage>/access"`
#### Invoke the Powerhell Script
Start a PowerShell Session, I use PowerShell Core and retrieve the help for the script:


`help ./Transfer-Files.ps1`

## Further Information
Please read my article with the same title on [Medium](https://medium.com/@daniel-ilie)

Thank you and have fun!
