import json

def lambda_handler(event, context):
    print("Function name:", context.function_name)
    print("Invoked ARN:", context.invoked_function_arn)
    print("Log stream name:", context.log_stream_name)
    print("Log group name:",  context.log_group_name)
    print("Request ID:",context.aws_request_id)
    print("Mem. limits(MB):", context.memory_limit_in_mb)
    
    if event["GUID"] == "Exception":
        a = 5 / "w"
    
    elif event["GUID"] == "RaisedException":
        retVal = {
                "context": {
                    "EndPoint": "My Endpoint",
                    "LoadCase": 123,
                    "Id": "AA-BB"
                    
                },
                "message": "My Message",
                "type": "Exception",
                "code": 502
            
        }
        raise Exception(json.dumps(retVal))

    elif event["GUID"] == "Error":
        retVal = {
                "context": {
                    "EndPoint": "My Endpoint",
                    "LoadCase": 123,
                    "Id": "AA-BB"
                    
                },
                "message": "My Message",
                "type": "Error",
                "code": 400
            
        }
        raise Exception(json.dumps(retVal))
    
    retVal = {
            "context": {
                "EndPoint": "My Endpoint",
                "LoadCase": 123,
                "Id": "AA-BB"
                
            },
            "message": "All is Ok",
            "type": "Info",
            "code": 200
        
    }
    return retVal
