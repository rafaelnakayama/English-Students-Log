import students_functions as sf
import csv
import os
import datetime

def main_menu():
    Check = False

    # meus_alunos = []

    hoje = datetime.datetime.now()

    print("\n__ MENU PRINCIPAL __\n")
    print("1) Cadastrar alunos")
    print("2) Visualizar alunos")
    print("3) Sair")

    print(f"\n" + hoje.strftime("%x"))

    while (Check == False):
        try:
            option = int(input("\nSelecione uma das opcoes Acima: "))

            if option == 1:

                nome_do_aluno = str(input("Informe o nome do aluno: "))

                status_do_aluno = str(input("Este aluno está tendo aulas? (S/N): ")).upper()
                if status_do_aluno == "S":
                    status_do_aluno = "Ativo"
                elif status_do_aluno == "N":
                    status_do_aluno = "Deligado"
                else:
                    status_do_aluno = "UNKNOWN"

                aulas_assistidas = int(input("Informe quantas aulas o aluno assistiu: "))

                data_do_pagamento = str(input("Informe a data do pagamento: "))

                nivel_do_aluno = str(input("Informe o nível do aluno: "))

                # Caminho para evitar erros em outros diretorios
                caminho_csv = os.path.join(os.path.dirname(__file__), "data", "students.csv")

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
  
                    escritor.writerow({'Nome': f'{nome_do_aluno}', 
                                       'Status': f'{status_do_aluno}', 
                                       'Aulas': f'{aulas_assistidas}', 
                                       'Dia do Pagamento': f'{data_do_pagamento}', 
                                       'Nivel': f'{nivel_do_aluno}'})

            elif option == 2:
                # Abre e faz a leitura do .csv
                with open(caminho_csv, newline='') as arquivocsv:
                    leitor_csv = csv.DictReader(arquivocsv, delimiter=' ', quotechar='|')
                    for linha in leitor_csv:
                        print(', '.join(linha))

            elif option == 3:
                break

            else:
                print(f"A Opção '{option}' não exite.")

        except:
            print(f"Este Caractere provavelmente não é inteiro.")
            Check = False
    
main_menu()