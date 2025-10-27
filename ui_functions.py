"""
This file contains the User Interface functions
"""

import datetime
import students_functions as sf

# Pedi para o chat gpt gerar cores para serem inseridos nos prints
CORES = {
    "reset": "\033[0m",       # Reseta para cor padrão
    "preto": "\033[30m",
    "vermelho": "\033[31m",
    "verde": "\033[32m",
    "amarelo": "\033[33m",
    "azul": "\033[34m",
    "roxo": "\033[35m",
    "ciano": "\033[36m",
    "branco": "\033[37m",

    # Versões em negrito
    "preto_b": "\033[1;30m",
    "vermelho_b": "\033[1;31m",
    "verde_b": "\033[1;32m",
    "amarelo_b": "\033[1;33m",
    "azul_b": "\033[1;34m",
    "roxo_b": "\033[1;35m",
    "ciano_b": "\033[1;36m",
    "branco_b": "\033[1;37m",

    # Fundos coloridos
    "fundo_preto": "\033[40m",
    "fundo_vermelho": "\033[41m",
    "fundo_verde": "\033[42m",
    "fundo_amarelo": "\033[43m",
    "fundo_azul": "\033[44m",
    "fundo_roxo": "\033[45m",
    "fundo_ciano": "\033[46m",
    "fundo_branco": "\033[47m",
}


def menu_interface():

    hoje = datetime.datetime.now()

    print(f"\n{CORES['azul_b']}MENU PRINCIPAL{CORES['reset']}\n")
    print(f"{CORES['amarelo']}1) Cadastrar alunos{CORES['reset']}")
    print(f"{CORES['amarelo']}2) Visualizar alunos{CORES['reset']}")
    print(f"{CORES['amarelo']}3) Editar Informações{CORES['reset']}")
    print(f"{CORES['amarelo']}4) Remover Aluno{CORES['reset']}")
    print(f"{CORES['amarelo']}5) Sair do programa{CORES['reset']}")

    print(f"\n" + hoje.strftime("%x"))


def menu_option_3():

    print(f"\n{CORES['ciano_b']}MENU EDITAR{CORES['reset']}\n")
    print(f"{CORES['amarelo']}1) Alterar Nome{CORES['reset']}")
    print(f"{CORES['amarelo']}2) Alterar Status{CORES['reset']}")
    print(f"{CORES['amarelo']}3) Alterar Quantidade de Aulas{CORES['reset']}")
    print(f"{CORES['amarelo']}4) Alterar Dia do Pagamento{CORES['reset']}")
    print(f"{CORES['amarelo']}5) Alterar Nível{CORES['reset']}")

def inputs_cadastro():

    # Nome
    nome_aluno = str(input(f"{CORES['verde']}Informe o nome do aluno(a): {CORES['reset']}"))
    sf.aluno_existe(nome_aluno)

    while(sf.aluno_existe == True):
        print(f"{CORES['vermelho']}Este aluno já está cadastrado.{CORES['reset']}")
        nome_aluno = str(input(f"{CORES['verde']}Informe o nome do aluno(a): {CORES['reset']}"))

    # Status
    status_aluno = str(input(f"{CORES['verde']}Status do Aluno (A - Ativo, D - Desligado): {CORES['reset']}")).upper()
    if status_aluno == "A":
        status_aluno = "Ativo"
    elif status_aluno == "D":
        status_aluno = "Deligado"
    else:
        status_aluno = "UNKNOWN"

    # Aulas
    aulas_aluno = int(input(f"{CORES['verde']}Aulas assistidas: {CORES['reset']}"))

    while(aulas_aluno < 0):
        print(f"{CORES['vermelho']}Este valor não pode ser Negativo.{CORES['reset']}")
        aulas_aluno = int(input(f"{CORES['verde']}Aulas assistidas: {CORES['reset']}"))
        
    # Pagamento
    pagamento_aluno = str(input(f"{CORES['verde']}Dia e mês do último pagamento: {CORES['reset']}"))

    # Nivel
    nivel_aluno = str(input(f"{CORES['verde']}Nível do aluno: {CORES['reset']}"))

    return nome_aluno, status_aluno, aulas_aluno, pagamento_aluno, nivel_aluno

def inputs_editar():
    Check = False
    chave = None
    valor_atualizado = None

    while (Check == False):
        try:
            selecao = int(input("\n\033[35mSelecione um valor: \033[0m"))

            if selecao >= 1 and selecao <= 5:
                Check = True
            else:
                print("\033[1;31mUm valor entre 1 e 5 deve ser inserido.\033[1;31m")
                Check = False

        except ValueError:
            print("\033[1;31mO caractére inserido não é inteiro.\033[1;31m")
            Check = False
            continue
        except:
            print("\033[1;31mOutra coisa deu errada.\033[1;31m")
            Check = False
            continue

    if selecao == 1:
        chave = 'Nome'
        valor_atualizado = str(input(f"{CORES['verde']}Inserir novo nome: {CORES['reset']}"))

    elif selecao == 2:
        chave = 'Status'
        valor_atualizado = str(input(f"{CORES['verde']}Status: {CORES['reset']}"))

    elif selecao == 3:
        chave = 'Aulas'
        valor_atualizado = int(input(f"{CORES['verde']}Aulas assistidas: {CORES['reset']}"))
        while(valor_atualizado < 0):
            print(f"{CORES['vermelho']}Este valor não pode ser Negativo.{CORES['reset']}")
            valor_atualizado = int(input(f"{CORES['verde']}Aulas assistidas: {CORES['reset']}"))

    elif selecao == 4:
        chave = 'Dia do Pagamento'
        valor_atualizado = str(input(f"{CORES['verde']}Novo dia de pagamento: {CORES['reset']}"))

    elif selecao == 5:
        chave = 'Nivel'
        valor_atualizado = str(input(f"{CORES['verde']}Nível: {CORES['reset']}"))

    return chave, valor_atualizado