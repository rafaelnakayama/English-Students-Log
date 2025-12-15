import os
import pandas as pd
import utils
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

caminho_token = utils.writable_path("data", "token.json")
caminho_cred = utils.resource_path("data", "credenciais.json")

PASTA_CURSO_ID = "10n1IG9bxWjaR_V5bpw6p_1Y32SrhEdCY"

def autenticar():
    credenciais = None

    if os.path.exists(caminho_token):
        credenciais = Credentials.from_authorized_user_file(caminho_token, SCOPES)

    if not credenciais or not credenciais.valid:
        if credenciais and credenciais.expired and credenciais.refresh_token:
            credenciais.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(caminho_cred, SCOPES)
            if getattr(sys, "frozen", False):
                try:
                    credenciais = flow.run_local_server(port=0)
                except Exception as e:
                    print(f"Erro ao tentar autenticar via EXE: {e}")
                    raise
            else:
                credenciais = flow.run_local_server(port=0)

        with open(caminho_token, 'w') as token:
            token.write(credenciais.to_json())

    return credenciais

def get_service():
    credenciais = autenticar()
    return build('drive', 'v3', credentials=credenciais)

def csv_existe(service):

    if not os.path.exists(utils.writable_path("data", "aulas.csv")):
        criar_csvs(service)

    elif not os.path.exists(utils.writable_path("data", "textos.csv")):
        criar_csvs(service)

    elif not os.path.exists(utils.writable_path("data", "exercicios.csv")):
        criar_csvs(service)
    else:
        pass

def criar_csvs(service):
    try:
        results = service.files().list(
            pageSize=50,
            fields="files(id,name)",
            q=f"'{PASTA_CURSO_ID}' in parents and trashed = false"
        ).execute()
    except Exception as e:
        print(f"ERRO! Falha ao acessar o Drive: {e}")
        results = {"files": []}

    items = results.get("files", [])

    todas_aulas = []
    todos_textos = []
    todas_atividades = []

    for item in items:
        nome_loop = item.get("name", "")
        id_loop = item.get("id", "")

        try:
            sub = service.files().list(
                fields="files(id,name)",
                q=f"'{id_loop}' in parents and trashed = false"
            ).execute().get("files", [])
        except:
            sub = []

        if nome_loop.endswith("(Aulas)"):
            todas_aulas.extend(sub)

        elif nome_loop.endswith("(Textos)"):
            todos_textos.extend(sub)

        elif nome_loop.endswith("(Atividades)"):
            todas_atividades.extend(sub)

    aulas_df = pd.DataFrame(todas_aulas)

    if not aulas_df.empty and "name" in aulas_df.columns:
        try:
            aulas_df['numero'] = (
                aulas_df['name']
                .str.extract(r'Class\s+(\d+(?:\.\d+)?)')
                .astype(float)
            )
            aulas_df = aulas_df.sort_values(by="numero", ascending=True)
            aulas_df.drop(columns=['numero'], inplace=True)
        except:
            pass

    aulas_df.to_csv(utils.writable_path("data", "aulas.csv"), index=False)

    textos_df = pd.DataFrame(todos_textos)

    if not textos_df.empty and "name" in textos_df.columns:
        try:
            textos_df = textos_df.sort_values(by="name")
        except:
            pass

    textos_df.to_csv(utils.writable_path("data", "textos.csv"), index=False)

    atividades_df = pd.DataFrame(todas_atividades)

    if not atividades_df.empty and "name" in atividades_df.columns:
        try:
            atividades_df = atividades_df.sort_values(by="name")
        except:
            pass

    atividades_df.to_csv(utils.writable_path("data", "exercicios.csv"), index=False)

    print("\n Os CSVs foram criados/atualizados com sucesso\n")

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
            q=f"'{folder_id}' in parents and trashed = false"
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

    if novos_ids_aulas:
        aulas_local = pd.concat([aulas_local, pd.DataFrame(novos_ids_aulas)], ignore_index=True)
        aulas_local.to_csv(caminho_aulas, index=False)

    if novos_ids_textos:
        textos_local = pd.concat([textos_local, pd.DataFrame(novos_ids_textos)], ignore_index=True)
        textos_local.to_csv(caminho_textos, index=False)

    if novos_ids_exercicios:
        atividades_local = pd.concat([atividades_local, pd.DataFrame(novos_ids_exercicios)], ignore_index=True)
        atividades_local.to_csv(caminho_exercicios, index=False)
