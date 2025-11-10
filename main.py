import students_functions as sf
import ui_functions as ui
import classes_functions as cf

def main_menu():
    Check = False

    sf.verificar_csv()

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
            id_aluno, nome_aluno, status_aluno, aulas_aluno, pagamento_aluno, nivel_aluno = ui.inputs_cadastro()

            novo_Aluno = sf.cadastrar_aluno(id_aluno,
                                            nome_aluno, 
                                            status_aluno, 
                                            aulas_aluno,
                                            pagamento_aluno,
                                            nivel_aluno,)
            print("\n")
            ui.menu_interface()

        elif option == 2:
            sf.visualizar_alunos()
            ui.menu_interface()

        elif option == 3:
            # Chama o menu de Editar Aluno
            ui.menu_option_3()

            # Nome
            alterar_por_nome = str(input("\n\033[38;5;208mInforme o do aluno a ser editado: \033[0m"))
            sf.aluno_existe(alterar_por_nome)

            while (sf.aluno_existe(alterar_por_nome) == False):
                print("\033[1;31mEste aluno não está no banco de dados.\033[0m")
                alterar_por_nome = str(input("\033[32mInforme o nome do aluno: \033[0m"))

            # Chama os inputs do editar, e associa os valores do return às variaveis locais.
            chave, valor_atualizado = ui.inputs_editar()

            sf.editar_aluno(alterar_por_nome, chave, valor_atualizado)

            print("\n")
            ui.menu_interface()

        elif option == 4:
            nome_aluno = str(input("\033[32mInforme o nome do aluno: \033[1;31m")).lower().strip()
            sf.aluno_existe(nome_aluno)

            while (sf.aluno_existe(nome_aluno) == False):
                print("\033[1;31mEste aluno não está no banco de dados.\033[1;31m")
                nome_aluno = str(input("\033[32mInforme o nome do aluno: \033[1;31m"))

            verifica = str(input(f"\033[41mTEM CERTEZA QUE DESEJA APAGAR O ALUNO {nome_aluno} (S/N): \033[0m")).lower().strip()
            while (verifica != "s" and verifica != "n"):
                print("\033[1;31mOpcao Invalida.\033[1;31m")
                verifica = str(input(f"\033[41mTEM CERTEZA QUE DESEJA APAGAR O ALUNO {nome_aluno} (S/N): \033[0m")).lower().strip()

            if verifica == "s":
                nome_check = str(input(f"\033[41mDIGITE O NOME {nome_aluno} PARA APAGAR: \033[0m")).lower().strip()
                while(nome_check != nome_aluno):
                    nome_check = str(input(f"\033[41mDIGITE O NOME {nome_aluno} PARA APAGAR: \033[0m")).lower().strip()
            else:
                print("\n\033[1;35mOperação cancelada. Retornando ao menu principal...\033[0m")
                ui.menu_interface()
                continue

            id_aluno = sf.pegar_id_por_nome(nome_check)

            sf.remover_aluno(nome_check, id_aluno)

            print("\n")
            ui.menu_interface()

        elif option == 5:
            # chama o menu Materiais
            ui.menu_materiais()

            Validar = False
            
            while(Validar == False):
                try:
                    opcao = int(input("\n\033[38;5;208mSelecione uma das opcoes acima: \033[0m"))
                except ValueError:
                    print("\033[1;31mO caractére inserido não é inteiro.\033[1;31m")
                    Validar = False
                    continue
                except:
                    print("\033[1;31mOutra coisa deu errada.\033[1;31m")
                    Validar = False
                    continue

                if opcao == 1:
                    tipo = cf.validar_tipo()
                    cf.visualizar_material(tipo)

                # opcao == 2 (viz) yet to be made

                elif opcao == 3:
                    nome_aluno_m = str(input("\033[32mInforme o nome do aluno: \033[1;31m")).lower().strip()
                    sf.aluno_existe(nome_aluno_m)

                    while (sf.aluno_existe(nome_aluno_m) == False):
                        print("\033[1;31mEste aluno não está no banco de dados.\033[1;31m")
                        nome_aluno_m = str(input("\033[32mInforme o nome do aluno: \033[1;31m"))

                    id_aluno_m = sf.pegar_id_por_nome(nome_aluno_m)
                    tipo_m = cf.validar_tipo()
                    
                    

                # opcao == 4 (remove) yet to be made

                elif opcao == 5:
                    print("\n\033[1;35mRetornando ao menu principal\033[1;35m")
                    Validar = True

                elif opcao == 6:
                    Validar = True
                    Check = True
                    print("\n\033[1;35mSaindo do programa...\033[1;35m")

                else:
                    print(f"\033[1;31mA Opção '{opcao}' não exite.\033[1;35m")

                if opcao == 1 or opcao == 2:
                    ui.menu_materiais()
                elif opcao == 5:
                    ui.menu_interface()
                else:
                    continue

        elif option == 6:
            print("\n\033[1;35mSaindo do programa...\033[1;35m")
            Check = True

        else:
            print(f"\033[1;31mA Opção '{option}' não exite.\033[1;35m")
    
main_menu()