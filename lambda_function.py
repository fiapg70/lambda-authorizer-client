import boto3
import json

def lambda_handler(event, context):
    cpf = body['cpf']
    senha = body['senha']
    # Substitua esses valores pelos seus próprios
    USER_POOL_ID = 'us-east-1_lLiNIC87U'
    CLIENT_ID = '67v6o5suqcos03dd1pev1pb7bj'
    USERNAME = cpf,
    PASSWORD = senha,

    # Inicializa o cliente Cognito
    client = boto3.client('cognito-idp')

    try:
        # Autentica o usuário no Amazon Cognito
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': USERNAME,
                'PASSWORD': PASSWORD
            },
            ClientId="67v6o5suqcos03dd1pev1pb7bj"
        )
        
        # Retorna o token de acesso se a autenticação for bem-sucedida
        if 'AuthenticationResult' in response:
            access_token = response['AuthenticationResult']['AccessToken']
            return {
                'statusCode': 200,
                'body': json.dumps({'access_token': access_token})
            }
        else:
            return {
                'statusCode': 401,
                'body': json.dumps({'message': 'Falha na autenticação'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error_message': str(e)})
        }
