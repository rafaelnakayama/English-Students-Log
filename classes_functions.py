"""
This file contains the features of the english materials
"""

import csv
import os
import pandas as pd
from tabulate import tabulate

# para caminhos
base_dir = os.path.dirname(__file__)
PASTA_DATA = 'data'

ARQUIVOS = {
    'aulas': os.path.join(base_dir, PASTA_DATA, 'aulas.csv'),
    'exercicios': os.path.join(base_dir, PASTA_DATA, 'exercicios.csv'),
    'textos': os.path.join(base_dir, PASTA_DATA, 'textos.csv')
}

def adicionar_material(id_param, tipo_param):
    # Os 3 caminhos do csv de cada aluno
    caminho_aulas_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_param}_aulas.csv")
    caminho_textos_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_param}_textos.csv")
    caminho_exercicios_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_param}_exercicios.csv")

    # Inicia as variaveis que vao receber diferentes valores dependendo dos inputs
    caminho_destino = None
    caminho_relativo = None
    nome_material = None
    print_ui = None

    if tipo_param == 1:
        caminho_relativo = ARQUIVOS['aulas']
        caminho_destino = caminho_aulas_aluno_csv
        print_ui = "Aula"

    elif tipo_param == 2:
        caminho_relativo = ARQUIVOS['textos']
        caminho_destino = caminho_textos_aluno_csv
        print_ui = "Texto"

    else:
        caminho_relativo = ARQUIVOS['exercicios']
        caminho_destino = caminho_exercicios_aluno_csv
        print_ui = "Exercicio"

    nome_material = str(input(f"\033[32mInformar o nome do {print_ui}: \033[1;31m")).strip()

    material_existe(nome_material, tipo_param) # Vai retornar True ou False
    while (material_existe(nome_material, tipo_param) == False):
        print(f"\033[1;31mEste {print_ui} não está no banco de dados.\033[1;31m")
        nome_material = str(input(f"\033[32mInforme o nome do {print_ui}: \033[1;31m"))

    id_material = pegar_id_por_nome_M(nome_material, caminho_relativo)

    # Adicionando ao respectivo csv
    df_origem = pd.read_csv(caminho_relativo)

    linha_copia = df_origem[df_origem['id'] == id_material].iloc[0] # Assegura com iloc[0] a captura de uma linha apenas

    df_destino = pd.read_csv(caminho_destino)

    df_destino.loc[len(df_destino)] = linha_copia
    df_destino.to_csv(caminho_destino, index=False)

    print(f"\nMaterial {nome_material} adicionado com sucesso ao historico do aluno com ID {id_param}.")

def pegar_id_por_nome_M(nome, caminho):

    df = pd.read_csv(caminho)

    df['name'] = df['name'].str.strip()

    # Filtra o aluno correspondente
    material_encontrado = df[df['name'] == nome]

    if not material_encontrado.empty:
        id_material = material_encontrado['id'].iloc[0]
        return id_material
    else:
        return None

def material_existe(nome_teste, tipo_param):
    caminho_relativo = None

    if tipo_param == 1:
        caminho_relativo = ARQUIVOS['aulas']
    elif tipo_param == 2:
        caminho_relativo = ARQUIVOS['textos']
    else:
        caminho_relativo = ARQUIVOS['exercicios']

    # dataframe
    df = pd.read_csv(caminho_relativo)

    df['name'] = df['name'].str.strip().str.lower()
    nome_teste = nome_teste.strip().lower()

    # este len serve para verificar se existe ao menos uma linha com o nome do material
    # se houver, este valor sera maior ou igual a 1, se nao, sera igual a zero
    # Com o return podemos retornar um valor booleano True se a condicional (>= 1) for verdadeira, e False caso contrario
    return len(df.loc[df['name'] == nome_teste]) >= 1

def validar_tipo():
    print("\033[38;5;208m(1) Aulas, (2) Textos ou (3) Exercicios\033[0m")
    Validar_2 = False
    while (Validar_2 == False):
        try:
            tipo_material = int(input("\n\033[38;5;208mSelecione o Material: \033[0m"))
            if tipo_material not in [1, 2, 3]:
                raise ValueError("fora_do_intervalo")
            Validar_2 = True
        except ValueError as e:
            if str(e) == "fora_do_intervalo":
                print("\033[1;31mO valor deve estar entre 1 e 3.\033[0m")
            else:
                print("\033[1;31mO caractére inserido não é inteiro.\033[0m")
            continue
        except Exception:
            print("\033[1;31mOutra coisa deu errada.\033[0m")
            continue
    
    return tipo_material

def visualizar_material(type):

    caminho_relativo = None

    if type == 1:
        caminho_relativo = ARQUIVOS['aulas']
    elif type == 2:
        caminho_relativo = ARQUIVOS['textos']
    else:
        caminho_relativo = ARQUIVOS['exercicios']

    # Abre e faz a leitura do .csv
    with open(caminho_relativo, newline='') as arquivocsv:

        leitor_csv = csv.DictReader(arquivocsv)

        headers = ['id','name']
        table = [] # Lista Vazia

        # Insere cada campo da linha especifica dentro da tabela
        for linha in leitor_csv:
            table.append([linha['id'], linha['name']])

        print(tabulate(table, headers=headers, tablefmt="fancy_grid")) # Usa o cabecalho headers que definimos anteriormente
        # Dispensa o uso de loop, printa cada linha uma vez assim como o cabecalho