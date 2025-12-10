import os
import pandas as pd
import utils

from google.auth.transport.requests import Request  # Requiscoes http
from google.oauth2.credentials import Credentials # Gerencia o token de Acesso
from google_auth_oauthlib.flow import InstalledAppFlow # controla o fluxo do OAuth (autenticacao via navegador)
from googleapiclient.discovery import build

# Define o Escopo (O que o programa pode fazer no drive) da API, neste caso apenas leitura
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

caminho_token = utils.writable_path("data", "token.json")

caminho_cred = utils.writable_path("data", "credenciais.json")

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
    aulas_df.to_csv(utils.writable_path("data", "aulas.csv"), index=False)

    textos_df = pd.DataFrame(todos_textos)
    textos_df = textos_df.sort_values(by="name", ascending=True)
    textos_df.to_csv(utils.writable_path("data", "textos.csv"), index=False)

    atividades_df = pd.DataFrame(todas_atividades)
    atividades_df = atividades_df.sort_values(by="name", ascending=True)
    atividades_df.to_csv(utils.writable_path("data", "exercicios.csv"), index=False)

criar_csvs(service)

def atualizar_csvs(service):

    results = service.files().list(
        pageSize=50,
        fields="files(id,name,parents)",
        q=f"'{PASTA_CURSO_ID}' in parents and trashed = false"
    ).execute()

    itens_nivel1 = results.get("files", [])

    novas_aulas = []
    novos_textos = []
    novas_atividades = []

    for item in itens_nivel1:
        nome = item["name"]
        folder_id = item["id"]

        sub = service.files().list(
            fields="files(id,name)",
            q=f"'{folder_id}' in parents and trashed = false and trashed = false"
        ).execute().get("files", [])

        if nome.endswith("(Aulas)"):
            novas_aulas = sub
        elif nome.endswith("(Textos)"):
            novos_textos = sub
        elif nome.endswith("(Atividades)"):
            novas_atividades = sub

    caminho_aulas = utils.writable_path("data", "aulas.csv")
    caminho_textos = utils.writable_path("data", "textos.csv")
    caminho_exercicios = utils.writable_path("data", "exercicios.csv")

    aulas_local = pd.read_csv(caminho_aulas)
    textos_local = pd.read_csv(caminho_textos)
    atividades_local = pd.read_csv(caminho_exercicios)

    set_local_aulas = set(aulas_local["id"])
    set_local_textos = set(textos_local["id"])
    set_local_atividades = set(atividades_local["id"])

    novos_ids_aulas = [i for i in novas_aulas if i["id"] not in set_local_aulas]
    novos_ids_textos = [i for i in novos_textos if i["id"] not in set_local_textos]
    novos_ids_exercicios = [i for i in novas_atividades if i["id"] not in set_local_atividades]

    if not novos_ids_aulas and not novos_ids_textos and not novos_ids_exercicios:
        return

    if novos_ids_aulas:
        aulas_local = pd.concat([aulas_local, pd.DataFrame(novos_ids_aulas)], ignore_index=True)
        aulas_local.to_csv(caminho_aulas, index=False)
        for item in novos_ids_aulas:
            print(f"📘 Nova aula adicionada: {item['name']}")

    if novos_ids_textos:
        textos_local = pd.concat([textos_local, pd.DataFrame(novos_ids_textos)], ignore_index=True)
        textos_local.to_csv(caminho_textos, index=False)
        for item in novos_ids_textos:
            print(f"📙 Novo texto adicionado: {item['name']}")

    if novos_ids_exercicios:
        atividades_local = pd.concat([atividades_local, pd.DataFrame(novos_ids_exercicios)], ignore_index=True)
        atividades_local.to_csv(caminho_exercicios, index=False)
        for item in novos_ids_exercicios:
            print(f"📒 Nova atividade adicionada: {item['name']}")

def get_service():
    credenciais = autenticar()
    return build('drive', 'v3', credentials=credenciais)