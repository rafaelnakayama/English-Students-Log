"""
Destinado as funcoes dos alunos
"""

import csv
import os

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
        leitor_csv = csv.DictReader(arquivocsv, delimiter=' ', quotechar='|')
        for linha in leitor_csv:
            print(', '.join(linha))