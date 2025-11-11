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
    caminho_relativo = None
    nome_material = None

    if tipo_param == 1:
        caminho_relativo = ARQUIVOS['aulas']

        nome_material = str(input("\033[32mInforme o nome da Aula: \033[1;31m")).strip()
        material_existe(nome_material, tipo_param)
        while (material_existe(nome_material, tipo_param) == False):
            print("\033[1;31mEsta aula não está no banco de dados.\033[1;31m")
            nome_material = str(input("\033[32mInforme o nome da Aula: \033[1;31m"))

    elif tipo_param == 2:
        caminho_relativo = ARQUIVOS['textos']

        nome_material = str(input("\033[32mInforme o nome do Texto: \033[1;31m")).strip()
        material_existe(nome_material, tipo_param)
        while (material_existe(nome_material, tipo_param) == False):
            print("\033[1;31mEste Texto não está no banco de dados.\033[1;31m")
            nome_material = str(input("\033[32mInforme o nome do Texto: \033[1;31m"))

    else:
        caminho_relativo = ARQUIVOS['exercicios']

        nome_material = str(input("\033[32mInforme o nome Exercicio: \033[1;31m")).strip()
        material_existe(nome_material, tipo_param)
        while (material_existe(nome_material, tipo_param) == False):
            print("\033[1;31mEste Exercicio não está no banco de dados.\033[1;31m")
            nome_material = str(input("\033[32mInforme o nome do Exercicio: \033[1;31m"))

    with open(caminho_relativo, newline='') as arquivocsv:
        df = pd.read_csv(arquivocsv)
        




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
    return len(df.loc[df['Nome'] == nome_teste]) >= 1


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