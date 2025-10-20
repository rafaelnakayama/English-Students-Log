import students_functions as sf
import datetime

def main_menu():
    Check = False

    hoje = datetime.datetime.now()

    print("\n__ MENU PRINCIPAL __\n")
    print("1) Cadastrar alunos")
    print("2) Visualizar alunos")
    print("3) Sair")

    print(hoje)

    while (Check == False):
        try:
            option = int(input("\nSelecione uma das opcoes Acima: "))

            if option == 1:
                nome_do_aluno = str(input("Informe o nome do aluno: "))
                status_do_aluno = str(input("Este aluno está tendo aulas? (S/N): ")).upper()
                if status_do_aluno == "S":
                    status_do_aluno == "Ativo"
                elif status_do_aluno == "N":
                    status_do_aluno == "Deligado"
                else:
                    status_do_aluno == "UNKNOWN"
                data_do_pagamento = str(input("Informe a data do pagamento: "))
                nivel_do_aluno = str(input("Informe o nome do aluno: "))

                cadastrar_aluno

            else:
                print(f"Caractere {option} inválido.")
        except:
            print(f"Caractere provavelmente não é inteiro.")
            Check = False
    

main_menu()