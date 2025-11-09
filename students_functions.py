"""
This file contains the features of the student
"""

import csv
import os
import pandas as pd

from tabulate import tabulate

# Caminhos para evitar erros em outros diretorios:

# Caminho csv do students
caminho_csv = os.path.join(os.path.dirname(__file__), "data", "students.csv")

# Caminho da pasta historico
historico_dir = os.path.join(os.path.dirname(__file__), "data", "historicos")

def cadastrar_aluno(id_param,nome_param, status_param, aulas_param, pagamento_param, nivel_param):
    # Variavel Booleana que retorna True o csv ja foi criado e False se ainda nao
    arquivo_existe = os.path.exists(caminho_csv)
                
    if arquivo_existe:
        vazio = os.path.getsize(caminho_csv)  # os.path.getsize ja pega o numero em bytes direto

    # Registra no .csv as informacoes, coloquei no modo append para acrescentar e nunca sobrescrever
    with open(caminho_csv, "a", newline='') as arquivocsv:

        chaves_csv = ["ID","Nome","Status","Aulas","Dia do Pagamento","Nivel"]
        escritor = csv.DictWriter(arquivocsv, fieldnames=chaves_csv)

        # Se o caminho nao existe ou existe mas esta vazio, escreva o cabecalho
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
    # Os 3 caminhos do csv de cada aluno
    caminho_aulas_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_param}_aulas.csv")
    caminho_textos_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_param}_textos.csv")
    caminho_exercicios_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_param}_exercicios.csv")

    # Verificando e criando os materiais:

    criar_csv_vazio(caminho_aulas_aluno_csv)
    criar_csv_vazio(caminho_textos_aluno_csv)
    criar_csv_vazio(caminho_exercicios_aluno_csv)

def criar_csv_vazio(caminho):
    vazio_material = 0

    # Verificando e criando csv:
    material_existe = os.path.exists(caminho)

    if material_existe:
        vazio_material = os.path.getsize(caminho)

    with open(caminho, "a", newline='') as material_csv:

        chaves_material_csv = ["id", "name"]
        escritor = csv.DictWriter(material_csv, fieldnames=chaves_material_csv)

        if material_existe == False or vazio_material == 0:
            escritor.writeheader()

def visualizar_alunos():
    # Abre e faz a leitura do .csv
    with open(caminho_csv, newline='') as arquivocsv:

        leitor_csv = csv.DictReader(arquivocsv)

        headers = ['ID','Nome', 'Status', 'Aulas Assistidas', 'Dia do Pagamento', 'Nível']
        table = [] # Lista Vazia

        # Insere cada campo da linha especifica dentro da tabela
        for linha in leitor_csv:
            table.append([linha['ID'], linha['Nome'], linha['Status'], linha['Aulas'], linha['Dia do Pagamento'], linha['Nivel']]) 

        print(tabulate(table, headers=headers, tablefmt="fancy_grid")) # Usa o cabecalho headers que definimos anteriormente
        # Dispensa o uso de loop, printa cada linha uma vez assim como o cabecalho

def remover_aluno(aluno, id_aluno):

    # Os 3 caminhos do csv de cada aluno
    caminho_aulas_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_aluno}_aulas.csv")
    caminho_textos_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_aluno}_textos.csv")
    caminho_exercicios_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_aluno}_exercicios.csv")

    # dataframes
    df = pd.read_csv(caminho_csv)

    # Remove do students.csv por nome
    df_remover_por_valor = df[df['Nome'] != f'{aluno}']
    df_remover_por_valor.to_csv("data/students.csv", index=False)

    os.remove(caminho_aulas_aluno_csv)
    os.remove(caminho_textos_aluno_csv)
    os.remove(caminho_exercicios_aluno_csv)

    print(f"\nSUCESSO! o aluno {aluno} foi removido com sucesso.")

def pegar_id_por_nome(nome):

    df = pd.read_csv(caminho_csv)

    df['Nome'] = df['Nome'].str.strip().str.lower()

    # Filtra o aluno correspondente
    aluno_encontrado = df[df['Nome'] == nome]

    if not aluno_encontrado.empty:
        id_aluno = aluno_encontrado['ID'].iloc[0]
        return id_aluno
    else:
        return None

def aluno_existe(nome_teste):
    # dataframe
    df = pd.read_csv(caminho_csv)

    df['Nome'] = df['Nome'].str.strip().str.lower()
    nome_teste = nome_teste.strip().lower()

    # este len serve para verificar se existe ao menos uma linha com o nome do aluno informado
    # se houver, este valor sera maior ou igual a 1, se nao, sera igual a zero
    # Com o return podemos retornar um valor booleano True se a condicional (>= 1) for verdadeira, e False caso contrario
    return len(df.loc[df['Nome'] == nome_teste]) >= 1

def editar_aluno(nome_chave, key, new_value):
    # dataframe
    df = pd.read_csv(caminho_csv)
    
    # Colocando strip() e lower() para evitar erros de espacos inuteis e erros de case sensitive respectivamente
    df['Nome'] = df['Nome'].str.strip().str.lower()
    nome_chave = nome_chave.strip().lower()

    df.loc[df['Nome'] == nome_chave, key] = new_value
    df.to_csv("data/students.csv", index=False)

def verificar_csv():

    header = ['ID', 'Nome', 'Status', 'Aulas', 'Dia do Pagamento', 'Nivel']

    # Verifica se o arquivo existe
    if not os.path.exists(caminho_csv):
        with open(caminho_csv, mode='w', newline='', encoding='utf-8') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(header) # Insere o header
        print("O arquivo foi criado do zero com cabecalho padrao.")

    # Se nao existe mas estiver vazio (tamanho de 0 bytes), adicione o cabecalho padrao
    elif os.path.getsize(caminho_csv) == 0:
        with open(caminho_csv, mode='w', newline='', encoding='utf-8') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(header) # Insere o header
        print("O arquivo estava vazio, o cabecalho foi criado.")