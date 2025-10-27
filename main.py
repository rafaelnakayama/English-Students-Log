import students_functions as sf
import ui_functions as ui

def main_menu():
    Check = False

    ui.menu_interface()

    while (Check == False):
        try:
            option = int(input("\n\033[32mSelecione uma das opcoes acima: \033[0m"))
        except ValueError:
            print("\033[1;31mO caractére inserido não é inteiro.\033[1;31m")
            Check = False
            continue
        except:
            print("\033[1;31mOutra coisa deu errada.\033[1;31m")
            Check = False
            continue

        if option == 1:
            # Captura os valores que existem dentro de ui.inputs_cadastro()
            nome_aluno, status_aluno, aulas_aluno, pagamento_aluno, nivel_aluno = ui.inputs_cadastro()

            novo_Aluno = sf.cadastrar_aluno(nome_aluno, 
                                            status_aluno, 
                                            aulas_aluno,
                                            pagamento_aluno,
                                            nivel_aluno,)

        elif option == 2:
            sf.visualizar_alunos()

        elif option == 3:
            # Nome
            alterar_por_nome = str(input("\033[32mInforme o nome deste aluno: \033[0m"))
            sf.aluno_existe(alterar_por_nome)

            while (sf.aluno_existe(alterar_por_nome) == False):
                print("\033[1;31mEste aluno não está no banco de dados.\033[0m")
                alterar_por_nome = str(input("\033[32mInforme o nome do aluno: \033[0m"))
            
            # Chama o menu de Editar Aluno
            ui.menu_option_3()

            # Chama os inputs do editar, e associa os valores do return às variaveis locais.
            chave, valor_atualizado = ui.inputs_editar()

            sf.editar_aluno(alterar_por_nome, chave, valor_atualizado)

        elif option == 4:
            nome_aluno = str(input("\033[32mInforme o nome do aluno: \033[1;31m"))
            sf.aluno_existe(nome_aluno)

            while (sf.aluno_existe(nome_aluno) == False):
                print("\033[1;31mEste aluno não está no banco de dados.\033[1;31m")
                nome_aluno = str(input("\033[32mInforme o nome do aluno: \033[1;31m"))

            sf.remover_aluno(nome_aluno)

        elif option == 5:
            print("\n\033[1;35mSaindo do programa...\033[1;35m")
            Check = True

        else:
            print(f"\033[1;31mA Opção '{option}' não exite.\033[1;35m")
    
main_menu()