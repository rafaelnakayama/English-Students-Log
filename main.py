import students_functions as sf
import ui_functions as ui

def main_menu():
    Check = False

    ui.menu_interface()

    while (Check == False):
        try:
            option = int(input("\nSelecione uma das opcoes Acima: "))
        except ValueError:
            print("Este Caractere provavelmente não é inteiro.")
            Check = False
            continue
        except:
            print(f"Outra coisa deu errada.")
            Check = False
            continue


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

            alterar_por_nome = str(input("Informe o nome do aluno: "))

            chave = None
            valor_atualizado = None

            ui.menu_option_3()

            selecao = int(input("Selecione um valor: "))

            if selecao == 1:
                chave = 'Nome'
                valor_atualizado = str(input("Insira o novo Nome: "))
            elif selecao == 2:
                chave = 'Status'
                valor_atualizado = str(input("Insira o novo Status: "))
            elif selecao == 3:
                chave = 'Aulas'
                valor_atualizado = int(input("Informe a quantidade de Aulas: "))
            elif selecao == 4:
                chave = 'Dia do Pagamento'
                valor_atualizado = str(input("Insira o novo dia de Pagamento: "))
            elif selecao == 5:
                chave = 'Nivel'
                valor_atualizado = str(input("Insira o novo Nivel: "))

            sf.editar_aluno(alterar_por_nome, chave, valor_atualizado)

        elif option == 4:
            nome_aluno = str(input("Informe o nome do aluno: "))
            sf.remover_aluno(nome_aluno)

        elif option == 5:
            print("\nSaindo do programa...")
            break

        else:
            print(f"A Opção '{option}' não exite.")
    
main_menu()