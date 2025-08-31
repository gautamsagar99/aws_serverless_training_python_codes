## Deploy this code in lambda function

# How to setup and run  the project

1. Create a identity in ses and send a test email
2. Create a IAM role for lambda to connect to SES.
3. Now deploy this code in lambda
4. update FROM_EMAIL and DEFAULT_TO in lambda environment variables
5. Test the lambda by sending a email
6. create a API Gateway with /send-email resource and method with POST and connect to lambda
7. deploy the api gateway in dev stage 
8. Take the APIG URL and test entire flow (APIG -> Lambda -> SES)