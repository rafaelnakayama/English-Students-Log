import csv
import os
import pandas as pd
import re
import utils

from tabulate import tabulate

ARQUIVOS = {
    'aulas': utils.resource_path("data", "aulas.csv"),
    'exercicios': utils.resource_path("data", "exercicios.csv"),
    'textos': utils.resource_path("data", "textos.csv")
}

def visualizar_material(tipo):      # Opcao 1 do menu materiais
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

        for linha in leitor_csv:
            table.append([linha['id'], linha['name']])

        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

def visualizar_historico(id_param, tipo):   # Opcao 2 do menu materiais
    if tipo == 1:
        caminho_relativo = utils.resource_path("data", "historicos", f"{id_param}_aulas.csv")
    elif tipo == 2:
        caminho_relativo = utils.resource_path("data", "historicos", f"{id_param}_textos.csv")
    else:
        caminho_relativo = utils.resource_path("data", "historicos", f"{id_param}_exercicios.csv")

    with open(caminho_relativo, newline='') as arquivocsv:

        leitor_csv = csv.DictReader(arquivocsv)

        headers = ['id','name']
        table = []

        for linha in leitor_csv:
            table.append([linha['id'], linha['name']])

        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

def adicionar_material(id_param, tipo_param):   # Opcao 3 do menu materiais
    if tipo_param == 1:
        caminho_origem = ARQUIVOS['aulas']
        caminho_destino = utils.writable_path("data", "historicos", f"{id_param}_aulas.csv")
        print_ui = "Aula"

    elif tipo_param == 2:
        caminho_origem = ARQUIVOS['textos']
        caminho_destino = utils.writable_path("data", "historicos", f"{id_param}_textos.csv")
        print_ui = "Texto"

    else:
        caminho_origem = ARQUIVOS['exercicios']
        caminho_destino = utils.writable_path("data", "historicos", f"{id_param}_exercicios.csv")
        print_ui = "Exercicio"

    nome_01 = str(input(f"\033[32mInformar o nome do {print_ui}: \033[1;31m")).strip()
    nome_inserido_normalizado = normalizar_nome_material(nome_01)

    material_existe(nome_inserido_normalizado, tipo_param)
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

def remover_do_historico(id_param, tipo_param):     # Opcao 4 do menu materiais
    if tipo_param == 1:
        caminho_relativo = utils.writable_path("data", "historicos", f"{id_param}_aulas.csv")
        print_ui = "Aula"
    elif tipo_param == 2:
        caminho_relativo = utils.writable_path("data", "historicos", f"{id_param}_textos.csv")
        print_ui = "Texto"
    else:
        caminho_relativo = utils.writable_path("data", "historicos", f"{id_param}_exercicios.csv")
        print_ui = "Exercicio"

    nome_remover = str(input(f"\033[32mInformar o nome do {print_ui}: \033[1;31m")).strip()
    nome_inserido_normalizado = normalizar_nome_material(nome_remover)

    material_existe(nome_inserido_normalizado, tipo_param)
    while (material_existe(nome_inserido_normalizado, tipo_param) == False):
        print(f"\033[1;31mEste {print_ui} não está no banco de dados.\033[1;31m")
        nome_01 = str(input(f"\033[32mInforme o nome do {print_ui}: \033[1;31m"))
        nome_inserido_normalizado = normalizar_nome_material(nome_01)

    id_material = pegar_id_por_nome_M(nome_inserido_normalizado, caminho_relativo)

    df = pd.read_csv(caminho_relativo)
    df_remover_por_valor = df[df['id'] != f'{id_material}']
    df_remover_por_valor.to_csv(caminho_relativo, index=False)

    print(f"\nMaterial {nome_inserido_normalizado} REMOVIDO com sucesso ao historico do aluno com ID {id_param}.")

def validar_tipo():     # Identifica o tipo de Material
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

def normalizar_nome_material(nome):     # normaliza o nome do material
    nome = nome.strip().lower()
    nome = re.sub(r'\.pdf$|\.txt$|\.docx$', '', nome)  # remove extensao se houver
    nome = re.sub(r'\s+', ' ', nome)  # normaliza espacos internos
    return nome

def pegar_id_por_nome_M(nome, caminho):     # recebe o nome e retorna o id com o input do nome
    df = pd.read_csv(caminho)

    df['name_norm'] = df['name'].apply(normalizar_nome_material)
    nome_norm = normalizar_nome_material(nome)

    material = df[df['name_norm'] == nome_norm]

    if not material.empty:
        return material.iloc[0]['id']

    return None

def material_existe(nome_teste, tipo_param):    # recebe o tipo e o nome do material e retorna se ele existe no .csv de registro
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
    if tipo_param == 1:
        caminho = utils.resource_path("data", "historicos", f"{id_param}_aulas.csv")
    elif tipo_param == 2:
        caminho = utils.resource_path("data", "historicos", f"{id_param}_textos.csv")
    else:
        caminho = utils.resource_path("data", "historicos", f"{id_param}_exercicios.csv")

    df = pd.read_csv(caminho)

    df['name_norm'] = df['name'].apply(normalizar_nome_material)
    nome_teste_norm = normalizar_nome_material(nome_teste)

    return (df['name_norm'] == nome_teste_norm).any()