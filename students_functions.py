import csv
import os
import pandas as pd
import utils

from tabulate import tabulate

caminho_csv = utils.resource_path(os.path.join("data", "students.csv"))
historico_dir = utils.resource_path(os.path.join("data", "historicos"))

def cadastrar_aluno(id_param,nome_param, status_param, aulas_param, pagamento_param, nivel_param):
    arquivo_existe = os.path.exists(caminho_csv)
                
    if arquivo_existe:
        vazio = os.path.getsize(caminho_csv)

    with open(caminho_csv, "a", newline='') as arquivocsv:

        chaves_csv = ["ID","Nome","Status","Aulas","Dia do Pagamento","Nivel"]
        escritor = csv.DictWriter(arquivocsv, fieldnames=chaves_csv)

        if arquivo_existe == False or vazio == 0:
            escritor.writeheader()
  
        escritor.writerow({'ID': f'{id_param}',
                           'Nome': f'{nome_param}', 
                           'Status': f'{status_param}', 
                           'Aulas': f'{aulas_param}', 
                           'Dia do Pagamento': f'{pagamento_param}', 
                           'Nivel': f'{nivel_param}'})
        
    historico_existe = os.path.exists(historico_dir)
    if historico_existe == False:
        os.makedirs(historico_dir, exist_ok=True)

    historico_creator(id_param)

def historico_creator(id_param):
    caminho_aulas_aluno_csv = utils.resource_path(
        os.path.join("data", "historicos", f"{id_param}_aulas.csv")
    )

    caminho_textos_aluno_csv = utils.resource_path(
        os.path.join("data", "historicos", f"{id_param}_textos.csv")
    )

    caminho_exercicios_aluno_csv = utils.resource_path(
        os.path.join("data", "historicos", f"{id_param}_exercicios.csv")
    )

    criar_csv_vazio(caminho_aulas_aluno_csv)
    criar_csv_vazio(caminho_textos_aluno_csv)
    criar_csv_vazio(caminho_exercicios_aluno_csv)

def criar_csv_vazio(caminho):
    vazio_material = 0
    material_existe = os.path.exists(caminho)

    if material_existe:
        vazio_material = os.path.getsize(caminho)

    with open(caminho, "a", newline='') as material_csv:

        chaves_material_csv = ["id", "name"]
        escritor = csv.DictWriter(material_csv, fieldnames=chaves_material_csv)

        if material_existe == False or vazio_material == 0:
            escritor.writeheader()

def visualizar_alunos():
    with open(caminho_csv, newline='') as arquivocsv:
        leitor_csv = csv.DictReader(arquivocsv)
        headers = ['ID','Nome', 'Status', 'Aulas Assistidas', 'Dia do Pagamento', 'Nível']
        table = [] 

        for linha in leitor_csv:
            table.append([linha['ID'], linha['Nome'], linha['Status'], linha['Aulas'], linha['Dia do Pagamento'], linha['Nivel']]) 

        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

def remover_aluno(aluno, id_aluno):
    if aluno == None:
        print("\n\033[1;35mOperação cancelada. Retornando ao menu principal...\033[0m")
    else:
        caminho_aulas_aluno_csv = utils.resource_path(
            os.path.join("data", "historicos", f"{id_aluno}_aulas.csv")
        )

        caminho_textos_aluno_csv = utils.resource_path(
            os.path.join("data", "historicos", f"{id_aluno}_textos.csv")
        )

        caminho_exercicios_aluno_csv = utils.resource_path(
            os.path.join("data", "historicos", f"{id_aluno}_exercicios.csv")
        )

        df = pd.read_csv(caminho_csv)

        df_remover_por_valor = df[df['Nome'] != f'{aluno}']
        df_remover_por_valor.to_csv(utils.resource_path("data/students.csv"), index=False)

        os.remove(caminho_aulas_aluno_csv)
        os.remove(caminho_textos_aluno_csv)
        os.remove(caminho_exercicios_aluno_csv)

        print(f"\nSUCESSO! o aluno {aluno} foi removido com sucesso.")

def pegar_id_por_nome(nome):
    df = pd.read_csv(caminho_csv)

    df['Nome'] = df['Nome'].str.strip().str.lower()

    aluno_encontrado = df[df['Nome'] == nome]

    if not aluno_encontrado.empty:
        id_aluno = aluno_encontrado['ID'].iloc[0]
        return id_aluno
    else:
        return None

def aluno_existe(nome_teste):
    df = pd.read_csv(caminho_csv)

    df['Nome'] = df['Nome'].str.strip().str.lower()
    nome_teste = nome_teste.strip().lower()

    return len(df.loc[df['Nome'] == nome_teste]) >= 1

def editar_aluno(nome_chave, key, new_value):
    df = pd.read_csv(caminho_csv)

    df['Nome'] = df['Nome'].str.strip().str.lower()
    nome_chave = nome_chave.strip().lower()

    df.loc[df['Nome'] == nome_chave, key] = new_value
    df.to_csv(caminho_csv, index=False)

def verificar_csv():

    header = ['ID', 'Nome', 'Status', 'Aulas', 'Dia do Pagamento', 'Nivel']

    if not os.path.exists(caminho_csv):
        with open(caminho_csv, mode='w', newline='', encoding='utf-8') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(header)
        print("O arquivo foi criado do zero com cabecalho padrao.")

    elif os.path.getsize(caminho_csv) == 0:
        with open(caminho_csv, mode='w', newline='', encoding='utf-8') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(header)
        print("O arquivo estava vazio, o cabecalho foi criado.")