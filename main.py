import students_functions as sf
import datetime

def main_menu():
    Check = False

    # meus_alunos = []

    hoje = datetime.datetime.now()

    print("\n__ MENU PRINCIPAL __\n")
    print("1) Cadastrar alunos")
    print("2) Visualizar alunos")
    print("3) Remover aluno'")
    print("4) Sair")

    print(f"\n" + hoje.strftime("%x"))

    while (Check == False):
        try:
            option = int(input("\nSelecione uma das opcoes Acima: "))

            if option == 1:

                nome_aluno = str(input("Informe o nome do aluno: "))

                status_aluno = str(input("Este aluno está tendo aulas? (S/N): ")).upper()
                if status_aluno == "S":
                    status_aluno = "Ativo"
                elif status_aluno == "N":
                    status_aluno = "Deligado"
                else:
                    status_aluno = "UNKNOWN"

                aulas_aluno = int(input("Informe quantas aulas o aluno assistiu: "))
                pagamento_aluno = str(input("Informe a data do pagamento: "))
                nivel_aluno = str(input("Informe o nível do aluno: "))

                novo_Aluno = sf.cadastrar_aluno(nome_aluno, 
                                                status_aluno, 
                                                aulas_aluno,
                                                pagamento_aluno,
                                                nivel_aluno,)

            elif option == 2:
                sf.visualizar_alunos()

            elif option == 3:
                nome_aluno = str(input("Informe o nome do aluno: "))
                sf.remover_aluno(nome_aluno)

            elif option == 4:
                break

            else:
                print(f"A Opção '{option}' não exite.")

        except:
            print(f"Este Caractere provavelmente não é inteiro.")
            Check = False
    
main_menu()