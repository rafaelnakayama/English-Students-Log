"""
This file contains the User Interface functions
"""

import datetime

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

    print(f"\n{CORES['ciano_b']}MENU PRINCIPAL{CORES['reset']}\n")
    print(f"{CORES['amarelo']}1) Cadastrar alunos{CORES['reset']}")
    print(f"{CORES['amarelo']}2) Visualizar alunos{CORES['reset']}")
    print(f"{CORES['amarelo']}3) Editar Informações{CORES['reset']}")
    print(f"{CORES['amarelo']}4) Remover Aluno{CORES['reset']}")
    print(f"{CORES['amarelo']}5) Sair do programa{CORES['reset']}")

    print(f"\n" + hoje.strftime("%x"))


def menu_option_3():

    print(f"\n{CORES['azul_b']}Selecione uma opção:{CORES['reset']}\n")
    print(f"{CORES['verde']}1) Alterar Nome{CORES['reset']}")
    print(f"{CORES['verde']}2) Alterar Status{CORES['reset']}")
    print(f"{CORES['verde']}3) Alterar Quantidade de Aulas{CORES['reset']}")
    print(f"{CORES['verde']}4) Alterar Dia do Pagamento{CORES['reset']}")
    print(f"{CORES['verde']}5) Alterar Nível{CORES['reset']}")