# short-examples
Short Examples...

## Integrating API Gateway - Lambda Responses
### Location
/APIG-Lambda
### Contents
- **lambda_function.py** lambda function code in Python 
- **DanielHTTP.yaml** SAM (serverless application model) template
- **DanielHTTP-prod-oas30-apigateway.yaml** API Gateway export in Open API 3 + APIGateway extensions.
### Usage
Create the API by importing it, after you have replaced the <region> and <accountId> with your own details. To do so:
1. Click on `Create API` in the API Gateway Service
2. Click on `Import` in the REST API Section (not private)
3. Select the `Import from Swagger or Open API 3` and paste in the code
4. Make sure the `Endpoint` is set to `Regional` and finalise the import.

Alternatively, you can create everything manually through the console by reading the article on Medium

