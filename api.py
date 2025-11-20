import os
import pandas as pd
import utils

from google.auth.transport.requests import Request  # Requiscoes http
from google.oauth2.credentials import Credentials # Gerencia o token de Acesso
from google_auth_oauthlib.flow import InstalledAppFlow # controla o fluxo do OAuth (autenticacao via navegador)
from googleapiclient.discovery import build

# Define o Escopo (O que o programa pode fazer no drive) da API, neste caso apenas leitura
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

caminho_token = utils.resource_path(os.path.join("data", "token.json"))

caminho_cred = utils.resource_path(os.path.join("data", "credenciais.json"))

PASTA_CURSO_ID = "10n1IG9bxWjaR_V5bpw6p_1Y32SrhEdCY"

def autenticar():
    credenciais = None

    if os.path.exists(caminho_token):
        credenciais = Credentials.from_authorized_user_file(caminho_token, SCOPES)
    # Se nao existir ou nao houverem credenciais validas disponiveis, o usuario ira logar.
    if not credenciais or not credenciais.valid:
        if credenciais and credenciais.expired and credenciais.refresh_token:
            credenciais.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(caminho_cred, SCOPES)
            credenciais = flow.run_local_server(port=0)
        # Salvar as credenciais para a proxima autenticacao
        with open(caminho_token, 'w') as token:
            token.write(credenciais.to_json())
    return credenciais

credenciais = autenticar()

service = build('drive', 'v3', credentials=credenciais)

def criar_csvs(service):

    results = service.files().list(
        pageSize=12, 
        fields="files(id,name)", 
        q= f"'{PASTA_CURSO_ID}' in parents and trashed = false"
    ).execute()

    items = results.get("files", [])

    todas_aulas = []
    todos_textos = []
    todas_atividades = []

    if not items:
        print("Nenhuma aula encontrada.")
        
    else:
        for item in items:

            nome_loop = item["name"]
            id_loop = item["id"]

            if nome_loop.endswith("(Aulas)"):
                results_aulas = service.files().list(
                    fields="files(id,name)", 
                    q= f"'{id_loop}' in parents and trashed = false"
                ).execute()

                items_aulas = results_aulas.get("files", [])
                todas_aulas.extend(items_aulas)

            elif nome_loop.endswith("(Textos)"):
                results_textos = service.files().list(
                    fields="files(id,name)", 
                    q= f"'{id_loop}' in parents and trashed = false"
                ).execute()

                items_textos = results_textos.get("files", [])
                todos_textos.extend(items_textos)

            elif nome_loop.endswith("(Atividades)"):
                results_atividades = service.files().list(
                    fields="files(id,name)", 
                    q= f"'{id_loop}' in parents and trashed = false"
                ).execute()

                items_atividades = results_atividades.get("files", [])
                todas_atividades.extend(items_atividades)

            else:
                pass

    aulas_df = pd.DataFrame(todas_aulas)
    # Extrai a parte 'Class' da string, transforma em float e dai ordena usando RE dentro do pandas
    aulas_df['numero'] = aulas_df['name'].str.extract(r'Class\s+(\d+(?:\.\d+)?)').astype(float)
    aulas_df = aulas_df.sort_values(by="numero", ascending=True)
    aulas_df.drop(columns=['numero'], inplace=True)
    aulas_df.to_csv(utils.resource_path("data/aulas.csv"), index=False)

    textos_df = pd.DataFrame(todos_textos)
    textos_df = textos_df.sort_values(by="name", ascending=True)
    textos_df.to_csv(utils.resource_path("data/textos.csv"), index=False)

    atividades_df = pd.DataFrame(todas_atividades)
    atividades_df = atividades_df.sort_values(by="name", ascending=True)
    atividades_df.to_csv(utils.resource_path("data/exercicios.csv"), index=False)

criar_csvs(service)