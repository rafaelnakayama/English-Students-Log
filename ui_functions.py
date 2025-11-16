"""
This file contains the User Interface functions
"""

import datetime
import students_functions as sf
import uuid

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

def menu_materiais():
    BOLD = "\033[1m"
    ORANGE_256 = "\033[38;5;208m"  # A common orange in 256-color palette
    RESET = "\033[0m"

    print(f"\n{ORANGE_256}{BOLD}_MENU AULAS_{RESET}\n")
    print(f"{ORANGE_256}1) Visualizar Material{CORES['reset']}")
    print(f"{ORANGE_256}2) Histórico de Aulas{CORES['reset']}")
    print(f"{ORANGE_256}3) Adicionar Aula{CORES['reset']}")
    print(f"{ORANGE_256}4) Remover Aula{CORES['reset']}")
    print(f"{ORANGE_256}5) Voltar{CORES['reset']}")
    print(f"{ORANGE_256}6) Sair{CORES['reset']}")

def menu_interface():

    hoje = datetime.datetime.now()

    print(f"\n{CORES['azul_b']}[MENU PRINCIPAL]{CORES['reset']}\n")
    print(f"{CORES['amarelo']}1) Cadastrar Aluno{CORES['reset']}")
    print(f"{CORES['amarelo']}2) Visualizar Aluno{CORES['reset']}")
    print(f"{CORES['amarelo']}3) Editar Aluno{CORES['reset']}")
    print(f"{CORES['amarelo']}4) Remover Aluno{CORES['reset']}")
    print(f"{CORES['amarelo']}5) Materiais{CORES['reset']}")
    print(f"{CORES['amarelo']}6) Sair do programa{CORES['reset']}")

    print(f"\n" + hoje.strftime("%x"))


def menu_option_3():

    print(f"\n{CORES['ciano_b']}_MENU EDITAR ALUNO_{CORES['reset']}\n")
    print(f"{CORES['amarelo']}1) Alterar Nome{CORES['reset']}")
    print(f"{CORES['amarelo']}2) Alterar Status{CORES['reset']}")
    print(f"{CORES['amarelo']}3) Alterar Quantidade de Aulas{CORES['reset']}")
    print(f"{CORES['amarelo']}4) Alterar Dia do Pagamento{CORES['reset']}")
    print(f"{CORES['amarelo']}5) Alterar Nível{CORES['reset']}")

def pegar_nome():
    nome_aluno = str(input("\033[32mInforme o nome do aluno: \033[1;31m")).lower().strip()
    sf.aluno_existe(nome_aluno)
    while (sf.aluno_existe(nome_aluno) == False):
        print(f"\033[1;31mO aluno(a) {nome_aluno} não está no banco de dados.\033[1;31m")
        nome_aluno = str(input("\033[32mInforme o nome do aluno: \033[1;31m"))

    return nome_aluno

def confirmar_remover(nome_aluno):
    verifica = str(input(f"\033[41mTEM CERTEZA QUE DESEJA APAGAR O ALUNO {nome_aluno} (S/N): \033[0m")).lower().strip()

    while (verifica != "s" and verifica != "n"):
        print("\033[1;31mOpcao Invalida.\033[1;31m")
        verifica = str(input(f"\033[41mTEM CERTEZA QUE DESEJA APAGAR O ALUNO {nome_aluno} (S/N): \033[0m")).lower().strip()

    if verifica == "s":
        nome_check = str(input(f"\033[41mDIGITE O NOME {nome_aluno} PARA APAGAR: \033[0m")).lower().strip()
        while(nome_check != nome_aluno):
            nome_check = str(input(f"\033[41mDIGITE O NOME {nome_aluno} PARA APAGAR: \033[0m")).lower().strip()
    else:
        nome_check = None

    return nome_check

def inputs_cadastro():

    # Gera o ID do aluno uuid.uuid4()
    id_aluno = str(uuid.uuid4())

    # Nome
    nome_aluno = str(input(f"{CORES['verde']}Informe o nome do aluno(a): {CORES['reset']}")).lower()
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

    return id_aluno, nome_aluno, status_aluno, aulas_aluno, pagamento_aluno, nivel_aluno

def inputs_editar():
    Check = False
    chave = None
    valor_atualizado = None

    while (Check == False):
        try:
            selecao = int(input("\033[1;32mSelecione um valor: \033[0m"))

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