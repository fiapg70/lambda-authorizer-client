import requests
import json

def lambda_handler(event, context):
    USER_POOL_ID = 'us-east-1_lLiNIC87U'
    CLIENT_ID = '67v6o5suqcos03dd1pev1pb7bj'

    auth_url = f'https://cognito-idp.us-east-1.amazonaws.com/{USER_POOL_ID}/oauth2/token'

    payload = {
        'grant_type': 'password',
        'client_id': 67v6o5suqcos03dd1pev1pb7bj,
        'username': 'rogerio.fontes@hotmail.com',
        'password': "@UrXMcHTKWEqAY6^W$"
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.post(auth_url, data=payload, headers=headers)

    if response.status_code == 200:
        return json.loads(response.text)['access_token']
    else:
        print("Erro:", response.text)
        return None

# Exemplo de uso
username = 'seu_nome_de_usuario'
password = 'sua_senha'
access_token = get_access_token(username, password)
if access_token:
    print("Token de acesso obtido:", access_token)
else:
    print("Falha ao obter o token de acesso.")
