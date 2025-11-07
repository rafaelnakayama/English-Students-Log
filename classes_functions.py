"""
This file contains the features of the english materials
"""

import csv
import os
import pandas as pd
import uuid
from tabulate import tabulate

# para caminhos
base_dir = os.path.dirname(__file__)
PASTA_DATA = 'data'

ARQUIVOS = {
    'aulas': os.path.join(base_dir, PASTA_DATA, 'aulas.csv'),
    'exercicios': os.path.join(base_dir, PASTA_DATA, 'exercicios.csv'),
    'textos': os.path.join(base_dir, PASTA_DATA, 'textos.csv')
}

# Criação automática dos CSVs se não existirem SVSVSVSV
def verificar_csvs_materiais():
    os.makedirs(PASTA_DATA, exist_ok=True)
    for nome, caminho in ARQUIVOS.items():
        if not os.path.exists(caminho):
            with open(caminho, "w", newline="", encoding="utf-8") as f:
                escritor = csv.writer(f)
                escritor.writerow(["ID", "Nome", "Nível"])
            print(f"[+] Criado arquivo: {caminho}")

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