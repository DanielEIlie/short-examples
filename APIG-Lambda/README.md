## Integrating API Gateway - Lambda Responses

[[_TOC_]]

### Location
/APIG-Lambda
### Contents
- **lambda_function.py** lambda function code in Python
- **DanielHTTP.yaml** SAM (serverless application model) template
- **DanielHTTP-prod-oas30-apigateway.yaml** API Gateway export in Open API 3 + APIGateway extensions.
### Usage
Create the API by importing it, after you have replaced the **region** and **accountId** fields in the YAML file with your own details. To do so:
1. Click on `Create API` in the API Gateway Service
2. Click on `Import` in the REST API Section (not private)
3. Select the `Import from Swagger or Open API 3` and paste in the code
4. Make sure the `Endpoint` is set to `Regional` and finalise the import.

Alternatively, you can create everything manually through the console by reading my article with the same title on [Medium](https://medium.com/@daniel.ilie0)

### Invocations

**curl --request POST --verbose https://****.execute-api.eu-west-1.amazonaws.com/prod/guid?GUID=Exception**
> POST /prod/guid?GUID=Exception HTTP/1.1
>
> Host: ****.execute-api.eu-west-1.amazonaws.com
>
> User-Agent: curl/7.55.1
>
> Accept: */*
>
> HTTP/1.1 500 Internal Server Error
>
> Date: Mon, 19 Oct 2020 10:15:24 GMT
>
> Content-Type: application/json
>
> Content-Length: 200
>
> Connection: keep-alive
>
>{"errorMessage":"unsupported operand type(s) for /: 'int' and 'str'","errorType":"TypeError","**stackTrace**":["  File \"/var/task/lambda_function.py\", line 12, in lambda_handler\n    a = 5 / \"w\"\n"]}

**curl --request POST --verbose https://****.execute-api.eu-west-1.amazonaws.com/prod/guid?GUID=RaisedException**
> POST /prod/guid?GUID=RaisedException HTTP/1.1
>
> Host: ****.execute-api.eu-west-1.amazonaws.com
>
> User-Agent: curl/7.55.1
>
> Accept: */*
>
> HTTP/1.1 502 Bad Gateway
>
> Date: Mon, 19 Oct 2020 10:15:53 GMT
>
> Content-Type: application/json
>
> Content-Length: 166
>
> Connection: keep-alive
>
>{
    "errorMessage": {"context": {"EndPoint": "My Endpoint", "LoadCase": 123, "RunAnalysisId": "AA-BB"}, "message": "My Message", "type": "**Exception**", "code": 502}
}

**curl --request POST --verbose https://****.execute-api.eu-west-1.amazonaws.com/prod/guid?GUID=Error**
> POST /prod/guid?GUID=Error HTTP/1.1
>
> Host: ****.execute-api.eu-west-1.amazonaws.com
>
> User-Agent: curl/7.55.1
>
> Accept: */*
>
> HTTP/1.1 400 Bad Request
>
> Date: Mon, 19 Oct 2020 10:21:04 GMT
>
> Content-Type: application/json
>
> Content-Length: 162
>
> Connection: keep-alive
>
>{
    "errorMessage": {"context": {"EndPoint": "My Endpoint", "LoadCase": 123, "RunAnalysisId": "AA-BB"}, "message": "My Message", "type": "**Error**", "code": 400}
}

**curl --request POST --verbose https://****.execute-api.eu-west-1.amazonaws.com/prod/guid?GUID=AnythingElse**
> POST /prod/guid?GUID=AnythingElse HTTP/1.1
>
> Host: ****.execute-api.eu-west-1.amazonaws.com
>
> User-Agent: curl/7.55.1
>
> Accept: */*
>
> HTTP/1.1 200 OK
>
> Date: Mon, 19 Oct 2020 10:21:16 GMT
>
> Content-Type: application/json
>
> Content-Length: 125
>
> Connection: keep-alive
>
>{"context":{"EndPoint":"My Endpoint","LoadCase":123,"RunAnalysisId":"AA-BB"},"message":"All is Ok","type":"**Info**","code":200}

