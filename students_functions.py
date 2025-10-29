"""
This file contains the main features of the program, such as the options available at the menu.
"""

import csv
import os
import pandas as pd
from tabulate import tabulate

# Caminho para evitar erros em outros diretorios
caminho_csv = os.path.join(os.path.dirname(__file__), "data", "students.csv")

def cadastrar_aluno(nome_param, status_param, aulas_param, pagamento_param, nivel_param):
    # Variavel Booleana que retorna True o csv ja foi criado e False se ainda nao
    arquivo_existe = os.path.exists(caminho_csv)
                
    if arquivo_existe:
        vazio = os.path.getsize(caminho_csv)  # os.path.getsize ja pega o numero em bytes direto

    # Registra no .csv as informacoes, coloquei no modo append para acrescentar e nunca sobrescrever
    with open(caminho_csv, "a", newline='') as arquivocsv:

        chaves_csv = ["Nome","Status","Aulas","Dia do Pagamento","Nivel"]
        escritor = csv.DictWriter(arquivocsv, fieldnames=chaves_csv)

        # Se o caminho nao existe ou existe mas esta vazio, escrevba o cabecalho
        if arquivo_existe == False or vazio == 0:
            escritor.writeheader()
  
        escritor.writerow({'Nome': f'{nome_param}', 
                           'Status': f'{status_param}', 
                           'Aulas': f'{aulas_param}', 
                           'Dia do Pagamento': f'{pagamento_param}', 
                           'Nivel': f'{nivel_param}'})

def visualizar_alunos():
    # Abre e faz a leitura do .csv
    with open(caminho_csv, newline='') as arquivocsv:
        contador = 0
        leitor_csv = csv.DictReader(arquivocsv)
        headers = ['Nome', 'Status', 'Aulas Assistidas', 'Dia do Pagamento', 'Nivel']
        for linha in leitor_csv:
            contador += 1
            table = [[linha['Nome'], linha['Status'], linha['Aulas'], linha['Dia do Pagamento'], linha['Nivel']]]
            if contador == 1:
                print(tabulate(table, headers, tablefmt="simple"))
            else:
                print(tabulate(table, tablefmt="simple"))


def remover_aluno(aluno):
    # dataframe
    df = pd.read_csv(caminho_csv)

    df_remover_por_valor = df[df['Nome'] != f'{aluno}']
    df_remover_por_valor.to_csv("data/students.csv", index=False)

    print(f"\nSUCESSO! o aluno {aluno} foi removido com sucesso.")

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