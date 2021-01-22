import boto3
from botocore.exceptions import ClientError
from urllib.parse import unquote_plus
from os import environ
from LambdaExceptions import PublishMessageRaiseException

region = environ['REGION']
costCenter = environ['COSTCENTER']
snsArn = environ['SNSALERT']
timeLimit = environ['TIMELIMIT']

def lambda_handler(event, context):
  lambdaName = context.function_name
  lambdaId = context.invoked_function_arn
  awsRequestId = context.aws_request_id
  awsAccountNo = lambdaId.split(":")[4]
  lambdaLogGroup = context.log_group_name

  oper = event['operation'].lower()
  if oper == 'read':
    clientoper = 'get_object'
  elif oper == 'write':
    clientoper = 'put_object'
  else:
    clientoper = None
    retVal = {
      "context": {
        "Function": lambdaName,
        "RequestedOperation": oper
        },
      "message": "invalid operation specified",
      "type": "Error",
      "code": 400
      }
    PublishMessageRaiseException(
      True, region, costCenter, snsArn,
      lambdaName, retVal)

  s3Client = boto3.client('s3', region_name=region)
  decoded_key = unquote_plus(event['key'])

  try:
    tempURL = s3Client.generate_presigned_url(
      ClientMethod=clientoper,
      Params={
        'Bucket': event['bucket'],
        'Key': decoded_key},
      ExpiresIn = timeLimit)
    retVal = {
      "context": {
        "Bucket": event['bucket'],
        "Function": lambdaName,
        "Key": decoded_key,
        "RequestedOperation": oper
        },
      "message": "URL issued",
      "type": "Info",
      "code": 200
      }
    PublishMessageRaiseException(
      False, region, costCenter, snsArn,
      lambdaName, retVal)
    # Do not publish the preSignedUrl to SNS
    retVal.update({"preSignedUrl": tempURL})
  except ClientError as e:
    retVal = {
      "context": {
        "Bucket": event['bucket'],
        "Function": lambdaName,
        "Key": decoded_key,
        "RequestedOperation": oper
        },
      "message": e.response['Error'],
      "type": "Exception",
      "code": 502
      }
    PublishMessageRaiseException(
      True, region, costCenter, snsArn,
      lambdaName, retVal)

  print(retVal)
  return retVal

