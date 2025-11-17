import csv
import os
import pandas as pd
import re

from tabulate import tabulate

# para caminhos
base_dir = os.path.dirname(__file__)
PASTA_DATA = 'data'

ARQUIVOS = {
    'aulas': os.path.join(base_dir, PASTA_DATA, 'aulas.csv'),
    'exercicios': os.path.join(base_dir, PASTA_DATA, 'exercicios.csv'),
    'textos': os.path.join(base_dir, PASTA_DATA, 'textos.csv')
}

"""
OPCAO 1 DO MENU MATERIAIS
"""

def visualizar_material(tipo):

    caminho_relativo = None

    if tipo == 1:
        caminho_relativo = ARQUIVOS['aulas']
    elif tipo == 2:
        caminho_relativo = ARQUIVOS['textos']
    else:
        caminho_relativo = ARQUIVOS['exercicios']

    with open(caminho_relativo, newline='') as arquivocsv:

        leitor_csv = csv.DictReader(arquivocsv)

        headers = ['id','name']
        table = []

        # Insere cada campo da linha especifica dentro da tabela tabulate
        for linha in leitor_csv:
            table.append([linha['id'], linha['name']])

        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

"""
OPCAO 2 DO MENU MATERIAIS
"""

def visualizar_historico(id_param, tipo):

    # Os 3 caminhos do csv de cada aluno
    caminho_aulas_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_param}_aulas.csv")
    caminho_textos_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_param}_textos.csv")
    caminho_exercicios_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_param}_exercicios.csv")

    caminho_relativo = None

    if tipo == 1:
        caminho_relativo = caminho_aulas_aluno_csv
    elif tipo == 2:
        caminho_relativo = caminho_textos_aluno_csv
    else:
        caminho_relativo = caminho_exercicios_aluno_csv

    with open(caminho_relativo, newline='') as arquivocsv:

        leitor_csv = csv.DictReader(arquivocsv)

        headers = ['id','name']
        table = []

        # Insere cada campo da linha especifica dentro da tabela tabulate
        for linha in leitor_csv:
            table.append([linha['id'], linha['name']])

        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

"""
OPCAO 3 DO MENU MATERIAIS
"""

def adicionar_material(id_param, tipo_param):
    # Os 3 caminhos do csv de cada aluno
    caminho_aulas_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_param}_aulas.csv")
    caminho_textos_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_param}_textos.csv")
    caminho_exercicios_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_param}_exercicios.csv")

    # Inicia as variaveis que vao receber diferentes valores dependendo dos inputs
    caminho_destino = None
    caminho_origem = None
    nome_01 = None
    print_ui = None

    if tipo_param == 1:
        caminho_origem = ARQUIVOS['aulas']
        caminho_destino = caminho_aulas_aluno_csv
        print_ui = "Aula"

    elif tipo_param == 2:
        caminho_origem = ARQUIVOS['textos']
        caminho_destino = caminho_textos_aluno_csv
        print_ui = "Texto"

    else:
        caminho_origem = ARQUIVOS['exercicios']
        caminho_destino = caminho_exercicios_aluno_csv
        print_ui = "Exercicio"

    nome_01 = str(input(f"\033[32mInformar o nome do {print_ui}: \033[1;31m")).strip()
    nome_inserido_normalizado = normalizar_nome_material(nome_01)

    material_existe(nome_inserido_normalizado, tipo_param) # Vai retornar True ou False
    while (material_existe(nome_inserido_normalizado, tipo_param) == False):
        print(f"\033[1;31mEste {print_ui} não está no banco de dados.\033[1;31m")
        nome_01 = str(input(f"\033[32mInforme o nome do {print_ui}: \033[1;31m"))
        nome_inserido_normalizado = normalizar_nome_material(nome_01)

    while (material_cadastrado(nome_inserido_normalizado, tipo_param, id_param) == True):
        print(f"\033[1;31mEste {print_ui} já foi cadastrado.\033[1;31m")
        nome_01 = str(input(f"\033[32mInforme o nome de outro {print_ui}: \033[1;31m"))
        nome_inserido_normalizado = normalizar_nome_material(nome_01)
        while (material_existe(nome_inserido_normalizado, tipo_param) == False):
            print(f"\033[1;31mEste {print_ui} não está no banco de dados.\033[1;31m")
            nome_01 = str(input(f"\033[32mInforme o nome do {print_ui}: \033[1;31m"))
            nome_inserido_normalizado = normalizar_nome_material(nome_01)

    id_material = pegar_id_por_nome_M(nome_inserido_normalizado, caminho_origem)

    # Adicionando ao respectivo csv
    df_origem = pd.read_csv(caminho_origem)

    linha_copia = df_origem[df_origem['id'] == id_material].iloc[0] # Assegura com iloc[0] a captura de uma linha apenas

    df_destino = pd.read_csv(caminho_destino)

    df_destino.loc[len(df_destino)] = linha_copia
    df_destino.to_csv(caminho_destino, index=False)

    print(f"\nMaterial {nome_inserido_normalizado} ADICIONADO com sucesso ao historico do aluno com ID {id_param}.")

"""
OPCAO 4 DO MENU MATERIAIS
"""

def remover_do_historico(id_param, tipo_param):
    # Os 3 caminhos do csv de cada aluno
    caminho_aulas_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_param}_aulas.csv")
    caminho_textos_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_param}_textos.csv")
    caminho_exercicios_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_param}_exercicios.csv")

    caminho_relativo = None
    nome_remover = None
    print_ui = None

    if tipo_param == 1:
        caminho_relativo = caminho_aulas_aluno_csv
        print_ui = "Aula"
    elif tipo_param == 2:
        caminho_relativo = caminho_textos_aluno_csv
        print_ui = "Texto"
    else:
        caminho_relativo = caminho_exercicios_aluno_csv
        print_ui = "Exercicio"

    nome_remover = str(input(f"\033[32mInformar o nome do {print_ui}: \033[1;31m")).strip()
    nome_inserido_normalizado = normalizar_nome_material(nome_remover)

    material_existe(nome_inserido_normalizado, tipo_param) # Vai retornar True ou False
    while (material_existe(nome_inserido_normalizado, tipo_param) == False):
        print(f"\033[1;31mEste {print_ui} não está no banco de dados.\033[1;31m")
        nome_01 = str(input(f"\033[32mInforme o nome do {print_ui}: \033[1;31m"))
        nome_inserido_normalizado = normalizar_nome_material(nome_01)

    id_material = pegar_id_por_nome_M(nome_inserido_normalizado, caminho_relativo)

    df = pd.read_csv(caminho_relativo)
    # Remove do .csv por nome
    df_remover_por_valor = df[df['id'] != f'{id_material}']
    df_remover_por_valor.to_csv(caminho_relativo, index=False)

    print(f"\nMaterial {nome_inserido_normalizado} REMOVIDO com sucesso ao historico do aluno com ID {id_param}.")

"""
Funções auxiliares:
"""

#Identifica o tipo de Material

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

# normaliza o nome do material

def normalizar_nome_material(nome):
    nome = nome.strip().lower()
    nome = re.sub(r'\.pdf$|\.txt$|\.docx$', '', nome)  # remove extensão se houver
    nome = re.sub(r'\s+', ' ', nome)  # normaliza espaços internos
    return nome

# recebe o nome e retorna o id com o input do nome

def pegar_id_por_nome_M(nome, caminho):
    df = pd.read_csv(caminho)

    df['name_norm'] = df['name'].apply(normalizar_nome_material)
    nome_norm = normalizar_nome_material(nome)

    material = df[df['name_norm'] == nome_norm]

    if not material.empty:
        return material.iloc[0]['id']

    return None

# recebe o tipo e o nome do material e retorna se ele existe no .csv de registro

def material_existe(nome_teste, tipo_param):
    if tipo_param == 1:
        caminho = ARQUIVOS['aulas']
    elif tipo_param == 2:
        caminho = ARQUIVOS['textos']
    else:
        caminho = ARQUIVOS['exercicios']

    df = pd.read_csv(caminho)

    df['name_norm'] = df['name'].apply(normalizar_nome_material)
    nome_teste_norm = normalizar_nome_material(nome_teste)

    return (df['name_norm'] == nome_teste_norm).any()

def material_cadastrado(nome_teste, tipo_param, id_param):

    # Os 3 caminhos do csv de cada aluno
    caminho_aulas_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_param}_aulas.csv")
    caminho_textos_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_param}_textos.csv")
    caminho_exercicios_aluno_csv = os.path.join(os.path.dirname(__file__), "data", "historicos", f"{id_param}_exercicios.csv")

    if tipo_param == 1:
        caminho = caminho_aulas_aluno_csv
    elif tipo_param == 2:
        caminho = caminho_textos_aluno_csv
    else:
        caminho = caminho_exercicios_aluno_csv

    df = pd.read_csv(caminho)

    df['name_norm'] = df['name'].apply(normalizar_nome_material)
    nome_teste_norm = normalizar_nome_material(nome_teste)

    return (df['name_norm'] == nome_teste_norm).any()