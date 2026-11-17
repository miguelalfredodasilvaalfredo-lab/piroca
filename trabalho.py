import json
import os
from datetime import datetime, timedelta

ARQUIVO = "biblioteca.json"


def carregar_dados():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    return {
        "livros": [],
        "emprestimos": []
    }


def salvar_dados():
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


dados = carregar_dados()


def cadastrar_livro():
    print("\n--- CADASTRO DE LIVRO ---")

    titulo = input("Título do livro: ")
    autor = input("Nome do autor: ")
    codigo = input("Código do livro: ")

    for livro in dados["livros"]:
        if livro["codigo"] == codigo:
            print("Já existe um livro com esse código!")
            return

    livro = {
        "codigo": codigo,
        "titulo": titulo,
        "autor": autor,
        "disponivel": True
    }

    dados["livros"].append(livro)
    salvar_dados()

    print("Livro cadastrado com sucesso!")


def listar_livros():
    print("\n--- LIVROS CADASTRADOS ---")

    if not dados["livros"]:
        print("Nenhum livro cadastrado.")
        return

    for livro in dados["livros"]:
        status = "Disponível" if livro["disponivel"] else "Emprestado"

        print(f"""
Código: {livro['codigo']}
Título: {livro['titulo']}
Autor: {livro['autor']}
Situação: {status}
--------------------------""")


def emprestar_livro():
    print("\n--- EMPRÉSTIMO DE LIVRO ---")

    codigo = input("Código do livro: ")
    aluno = input("Nome do aluno: ")

    for livro in dados["livros"]:
        if livro["codigo"] == codigo:

            if not livro["disponivel"]:
                print("Este livro já está emprestado!")
                return

            data_emprestimo = datetime.now()
            data_devolucao = data_emprestimo + timedelta(days=7)

            emprestimo = {
                "codigo": codigo,
                "titulo": livro["titulo"],
                "aluno": aluno,
                "data_emprestimo": data_emprestimo.strftime("%d/%m/%Y"),
                "data_devolucao": data_devolucao.strftime("%d/%m/%Y"),
                "devolvido": False
            }

            dados["emprestimos"].append(emprestimo)
            livro["disponivel"] = False

            salvar_dados()

            print("Empréstimo realizado com sucesso!")
            print("Data prevista para devolução:",
                  data_devolucao.strftime("%d/%m/%Y"))
            return

    print("Livro não encontrado!")


def devolver_livro():
    print("\n--- DEVOLUÇÃO DE LIVRO ---")

    codigo = input("Código do livro: ")
    aluno = input("Nome do aluno: ")

    for emprestimo in dados["emprestimos"]:
        if (emprestimo["codigo"] == codigo
                and emprestimo["aluno"].lower() == aluno.lower()
                and not emprestimo["devolvido"]):

            emprestimo["devolvido"] = True

            for livro in dados["livros"]:
                if livro["codigo"] == codigo:
                    livro["disponivel"] = True
                    break

            salvar_dados()

            print("Devolução realizada com sucesso!")
            return

    print("Empréstimo não encontrado!")


def historico_emprestimos():
    print("\n--- HISTÓRICO DE EMPRÉSTIMOS ---")

    if not dados["emprestimos"]:
        print("Nenhum empréstimo registrado.")
        return

    for emprestimo in dados["emprestimos"]:
        status = "Devolvido" if emprestimo["devolvido"] else "Pendente"

        print(f"""
Livro: {emprestimo['titulo']}
Aluno: {emprestimo['aluno']}
Empréstimo: {emprestimo['data_emprestimo']}
Devolução prevista: {emprestimo['data_devolucao']}
Situação: {status}
--------------------------""")


def menu():
    while True:
        print("""
====================================
   SISTEMA DE BIBLIOTECA ESCOLAR
====================================
1 - Cadastrar livro
2 - Listar livros
3 - Emprestar livro
4 - Devolver livro
5 - Histórico de empréstimos
0 - Sair
====================================
""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_livro()

        elif opcao == "2":
            listar_livros()

        elif opcao == "3":
            emprestar_livro()

        elif opcao == "4":
            devolver_livro()

        elif opcao == "5":
            historico_emprestimos()

        elif opcao == "0":
            print("Sistema encerrado. Até logo!")
            break

        else:
            print("Opção inválida! Tente novamente.")


menu()