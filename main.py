import students_functions as sf
import ui_functions as ui
import classes_functions as cf

from api import atualizar_csvs
from api import service

def main_menu():
    sf.verificar_csv()
    cf.verificar_anotacoes_csv()
    ui.menu_interface()
    sf.criar_pasta_historico()
    atualizar_csvs(service)

    while (True):
        try:
            option = int(input("\n\033[32mSelecione uma das opcoes acima: \033[0m"))
        except ValueError:
            print("\033[1;31mO caractére inserido não é inteiro.\033[1;31m")
            continue

        if option == 1:
            id_aluno, nome_aluno, status_aluno, aulas_aluno, pagamento_aluno, nivel_aluno = ui.inputs_cadastro()

            sf.cadastrar_aluno(id_aluno, nome_aluno, status_aluno, aulas_aluno, pagamento_aluno, nivel_aluno)
            
            print("\n")
            ui.menu_interface()

        elif option == 2:
            sf.visualizar_alunos()
            ui.menu_interface()

        elif option == 3:
            ui.menu_editar()

            print("")
            
            alterar_por_nome = ui.pegar_nome()

            chave, valor_atualizado = ui.inputs_editar()

            sf.editar_aluno(alterar_por_nome, chave, valor_atualizado)

            print("\n")
            ui.menu_interface()

        elif option == 4:
            nome_aluno = ui.pegar_nome()

            nome_check = ui.confirmar_remover(nome_aluno)

            id_aluno = sf.pegar_id_por_nome(nome_check)

            sf.remover_aluno(nome_check, id_aluno)

            ui.menu_interface()

        elif option == 5:
            ui.menu_materiais()
            Validar = False
            
            while(Validar == False):
                try:
                    opcao = int(input("\n\033[38;5;208mSelecione uma das opcoes acima: \033[0m"))
                except ValueError:
                    print("\033[1;31mO caractére inserido não é inteiro.\033[1;31m")
                    Validar = False
                    continue

                if opcao == 1:
                    tipo_v = cf.validar_tipo()
                    cf.visualizar_material(tipo_v)

                elif opcao == 2:
                    nome_aluno_historico = ui.pegar_nome()

                    id_aluno_historico = sf.pegar_id_por_nome(nome_aluno_historico)

                    tipo_historico = cf.validar_tipo()

                    cf.visualizar_historico(id_aluno_historico, tipo_historico)

                elif opcao == 3:
                    nome_aluno_adicionar = ui.pegar_nome()

                    id_aluno_adicionar = sf.pegar_id_por_nome(nome_aluno_adicionar)

                    tipo_adicionar = cf.validar_tipo()

                    cf.adicionar_material(id_aluno_adicionar, tipo_adicionar)

                    aulas_assistidas = ui.quantidade_aulas(id_aluno_adicionar)
                    sf.editar_aluno(nome_aluno_adicionar, 'Aulas', aulas_assistidas)
                    
                elif opcao == 4:
                    nome_aluno_remover = ui.pegar_nome()

                    id_aluno_remover = sf.pegar_id_por_nome(nome_aluno_remover)

                    tipo_remover = cf.validar_tipo()

                    cf.remover_do_historico(id_aluno_remover, tipo_remover)

                    aulas_assistidas = ui.quantidade_aulas(id_aluno_remover)
                    sf.editar_aluno(nome_aluno_remover, 'Aulas', aulas_assistidas)
                    
                elif opcao == 5:
                    opcao_lembretes = cf.notes_options()

                    if opcao_lembretes == 1:
                        cf.ler_anotacoes()
                    else:
                        nome_aluno_anotar = ui.pegar_nome()
                        id_aluno_anotar = sf.pegar_id_por_nome(nome_aluno_anotar)
                        cf.adicionar_lembrete(id_aluno_anotar)

                elif opcao == 6:
                    print("\n\033[1;35mRetornando ao menu principal\033[1;35m")
                    Validar = True

                else:
                    print(f"\033[1;31mA Opção '{opcao}' não exite.\033[1;35m")

                if opcao <= 5:
                    ui.menu_materiais()
                elif opcao == 6:
                    ui.menu_interface()
                else:
                    continue

        elif option == 6:
            print("\n\033[1;35mSaindo do programa...\033[1;35m")
            break
        else:
            print(f"\033[1;31mA Opção '{option}' não exite.\033[1;35m")
    
main_menu()