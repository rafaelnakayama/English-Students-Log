"""
Destinado as funcoes dos alunos
"""

def cadastrar_aluno(nome_aluno, status, qtd_aulas, pagamento_dia, nivel):
    aluno = {
        "Nome: " : nome_aluno,
        "Status:" : status,
        "Aulas Assistidas: " : qtd_aulas,
        "Data Pagamento: " : pagamento_dia,
        "Nível: " : nivel,
    }

    return aluno