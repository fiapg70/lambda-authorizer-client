import json
import boto3
import requests
import hmac
import hashlib
import base64

def lambda_handler(event, context):
    try:
        # Validar a presença dos campos cpf e senha no corpo do evento
        if 'body' not in event:
            raise ValueError('Corpo da requisição não encontrado')
        
        body = json.loads(event['body'])
        if 'cpf' not in body or 'senha' not in body:
            raise ValueError('CPF e/ou senha ausentes no corpo da requisição')
        
        cpf = body['cpf']
        senha = body['senha']
        
        # Iniciar autenticação com o pool de usuários Cognito
        client = boto3.client('cognito-idp')
        params = {
            'AuthFlow': 'USER_PASSWORD_AUTH',
            'ClientId': '67v6o5suqcos03dd1pev1pb7bj',
            #'UserPoolId': 'us-east-1_lLiNIC87U',
            'AuthParameters': {
                'USERNAME': cpf,
                'PASSWORD': senha,
                'USER_POOL_ID': 'us-east-1_lLiNIC87U',  # Adicione aqui o UserPoolId
                'SECRET_HASH': calculate_secret_hash(cpf, '67v6o5suqcos03dd1pev1pb7bj', '1o4t8vbak8i6fq1b34fs2a8gdl2t9pu6kcf79qkn833qe72qhp2q')
            }
        }
        response = client.initiate_auth(**params)
        token = response['AuthenticationResult']['AccessToken']
        
        # Chamada à API REST externa
        api_url = 'URL_DA_SUA_API_REST_EXTERN'
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
        payload = {
            'cpf': cpf,
            'senha': senha
        }
        response = requests.post(api_url, headers=headers, json=payload)
        
        # Verificar o status da resposta da API externa
        if response.ok:
            return {
                'statusCode': 200,
                'body': response.json()
            }
        else:
            return {
                'statusCode': response.status_code,
                'body': json.dumps({
                    'error': response.text
                })
            }
    except ValueError as ve:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': str(ve)
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

def calculate_secret_hash(username, client_id, client_secret):
    message = username + client_id
    dig = hmac.new(str(client_secret).encode('utf-8'), 
                   msg = str(message).encode('utf-8'), 
                   digestmod = hashlib.sha256).digest()
    return base64.b64encode(dig).decode()