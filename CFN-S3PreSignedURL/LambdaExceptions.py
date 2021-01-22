def PublishMessageTo(
  region,
  costCenter,
  snsArn,
  referredFrom,
  filterList,
  message):
  #region Doc
  """Publishes a message to the given SNS topic

  Parameters
  ----------
  region : [string]
      [AWS Region]

  costCenter : [string]
      [Cost Center]

  snsArn : [string]
      [SNS Topic Arn where this is published]

  referredFrom : [string]
      [This is where this was referred from]

  filterList : [list]
      [SNS Topic Filter List]

  message : [dict]
      [Actual Message to be sent]

  Returns
  -------
  [dict]
      [SNS.publish response]
  """
  #endregion
  import boto3
  import json

  sns = boto3.resource("sns", region_name=region)
  topic = sns.Topic(snsArn)
  filters = "/"
  filters += "/".join(filterList)
  subject = "/".join([
    filters,
    costCenter,
    region,
    referredFrom])
  jsonMsg = {
    "default": message,
    "email": message,
    "sqs": message,
    "lambda": message,
    "http": message,
    "https": message,
    "sms": message
    }

  response = topic.publish(
      Message=json.dumps(jsonMsg),
      Subject=subject,
      MessageStructure='json',
      MessageAttributes={
          'msgAtt': {
              'DataType': 'String.Array',
              'StringValue': str(filterList)
              }
          }
      )
  return response

def PublishMessageRaiseException(
  isException,
  region,
  costCenter,
  snsArn,
  referredFrom,
  message):
  #region Doc
  """Publishes a message to the given SNS topic, optionally raises an exception

  Parameters
  ----------
  isException : bool
      [Flag to indicate an exception must be raised]

  region : [string]
      [AWS Region]

  costCenter : [string]
      [Cost Center]

  snsArn : [string]
      [SNS Topic Arn where this is published]

  referredFrom : [string]
      [This is where this was referred from]

  message : [string]
      [Actual Message to be sent]


  Returns
  -------
  [None]
      [None]

  Raises
  ------
  Exception
      [Uses the actual message]
  """
  #endregion
  import json

  # Check if message has type key, if not add it and set value to Exception.
  msgType = message.get("type", None)
  if msgType == None:
    message.update({"type": "Exception"})

  pubmsg = json.dumps(message)
  msgId = PublishMessageTo(
    region, costCenter, snsArn, referredFrom,
    [message.get("type","Exception")], pubmsg)
  # Output to CloudWatch Logs.
  print(message)
  if isException:
    raise Exception(pubmsg)

  return None
