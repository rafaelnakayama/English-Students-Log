from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

import os
caminho_token = os.path.join(os.path.dirname(__file__), "token.json")
creds = Credentials.from_authorized_user_file(caminho_token)

# Cria o serviço do Google Drive
service = build("drive", "v3", credentials=creds)

# Faz a requisição para listar os 10 primeiros arquivos
results = service.files().list(
    pageSize=10, fields="files(id, name)"
).execute()

# Pega a lista de arquivos retornada
items = results.get("files", [])

# Exibe o resultado
if not items:
    print("Nenhum arquivo encontrado.")
else:
    print("Arquivos encontrados:")
    for item in items:
        print(f"{item['name']} ({item['id']})")