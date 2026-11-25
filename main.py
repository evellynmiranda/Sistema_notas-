
from alunos import (
    cadastrar_aluno,
    listar_alunos,
    buscar_aluno,
    atualizar_aluno,
    excluir_aluno
)

from turmas import (
    cadastrar_turma,
    listar_turmas,
    buscar_turma,
    atualizar_turma,
    excluir_turma
)

from disciplinas import (
    cadastrar_disciplina,
    listar_disciplinas,
    buscar_disciplina,
    atualizar_disciplina,
    excluir_disciplina
)

from turma_disciplinas import (
    vincular_disciplina,
    listar_disciplinas_turma,
    remover_disciplina_turma
)

from matriculas import (
    cadastrar_matricula,
    listar_matriculas,
    buscar_matricula,
    atualizar_matricula,
    excluir_matricula
)

from notas import (
    lancar_notas,
    consultar_boletim
)


def ler_nota(mensagem):
    valor = input(mensagem).strip()

    if valor == "":
        return None

    # Aceitar vírgula ou ponto como separador decimal.
    return float(valor.replace(",", "."))


def menu():
    while True:
        print("\n========== SISTEMA DE NOTAS ESCOLARES ==========")

        print("\n--- ALUNOS ---")
        print("1. Cadastrar aluno")
        print("2. Listar alunos")
        print("3. Buscar aluno")
        print("4. Atualizar aluno")
        print("5. Excluir aluno")

        print("\n--- TURMAS ---")
        print("6. Cadastrar turma")
        print("7. Listar turmas")
        print("8. Buscar turma")
        print("9. Atualizar turma")
        print("10. Excluir turma")

        print("\n--- DISCIPLINAS ---")
        print("11. Cadastrar disciplina")
        print("12. Listar disciplinas")
        print("13. Buscar disciplina")
        print("14. Atualizar disciplina")
        print("15. Excluir disciplina")

        print("\n--- DISCIPLINAS POR TURMA ---")
        print("16. Vincular disciplina a uma turma")
        print("17. Listar disciplinas de uma turma")
        print("18. Remover disciplina de uma turma")

        print("\n--- MATRÍCULAS ---")
        print("19. Cadastrar matrícula")
        print("20. Listar matrículas")
        print("21. Buscar matrícula")
        print("22. Atualizar matrícula")
        print("23. Excluir matrícula")

        print("\n--- NOTAS E BOLETIM ---")
        print("24. Lançar ou atualizar notas")
        print("25. Consultar boletim")

        print("\n0. Sair")
        print("================================================")

        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                nome = input("Nome do aluno: ").strip()
                data_nascimento = input(
                    "Data de nascimento (AAAA-MM-DD) ou Enter para deixar vazio: "
                ).strip()
                matricula = input("Matrícula escolar: ").strip()

                if data_nascimento == "":
                    data_nascimento = None

                cadastrar_aluno(nome, matricula, data_nascimento)

            elif opcao == "2":
                listar_alunos()

            elif opcao == "3":
                aluno_id = int(input("ID do aluno: "))
                buscar_aluno(aluno_id)

            elif opcao == "4":
                aluno_id = int(input("ID do aluno que deseja atualizar: "))
                nome = input("Novo nome: ").strip()
                data_nascimento = input(
                    "Nova data de nascimento (AAAA-MM-DD) ou Enter para deixar vazio: "
                ).strip()
                matricula = input("Nova matrícula escolar: ").strip()

                if data_nascimento == "":
                    data_nascimento = None

                atualizar_aluno(
                    aluno_id,
                    nome,
                    matricula,
                    data_nascimento
                )

            elif opcao == "5":
                aluno_id = int(input("ID do aluno que deseja excluir: "))
                excluir_aluno(aluno_id)

            elif opcao == "6":
                nome = input("Nome da turma: ").strip()
                ano_serie = input("Ano/série: ").strip()
                turno = input("Turno: ").strip()

                cadastrar_turma(nome, ano_serie, turno)

            elif opcao == "7":
                listar_turmas()

            elif opcao == "8":
                turma_id = int(input("ID da turma: "))
                buscar_turma(turma_id)

            elif opcao == "9":
                turma_id = int(input("ID da turma que deseja atualizar: "))
                nome = input("Novo nome da turma: ").strip()
                ano_serie = input("Novo ano/série: ").strip()
                turno = input("Novo turno: ").strip()

                atualizar_turma(turma_id, nome, ano_serie, turno)

            elif opcao == "10":
                turma_id = int(input("ID da turma que deseja excluir: "))
                excluir_turma(turma_id)

            elif opcao == "11":
                nome = input("Nome da disciplina: ").strip()
                cadastrar_disciplina(nome)

            elif opcao == "12":
                listar_disciplinas()

            elif opcao == "13":
                disciplina_id = int(input("ID da disciplina: "))
                buscar_disciplina(disciplina_id)

            elif opcao == "14":
                disciplina_id = int(
                    input("ID da disciplina que deseja atualizar: ")
                )
                nome = input("Novo nome da disciplina: ").strip()

                atualizar_disciplina(disciplina_id, nome)

            elif opcao == "15":
                disciplina_id = int(
                    input("ID da disciplina que deseja excluir: ")
                )
                excluir_disciplina(disciplina_id)

            elif opcao == "16":
                print("\nTurmas cadastradas:")
                listar_turmas()
                turma_id = int(input("\nID da turma: "))

                print("\nDisciplinas cadastradas:")
                listar_disciplinas()
                disciplina_id = int(input("\nID da disciplina: "))

                vincular_disciplina(turma_id, disciplina_id)

            elif opcao == "17":
                turma_id = int(input("ID da turma: "))
                listar_disciplinas_turma(turma_id)

            elif opcao == "18":
                turma_id = int(input("ID da turma: "))

                print("\nDisciplinas vinculadas à turma:")
                listar_disciplinas_turma(turma_id)

                disciplina_id = int(
                    input("\nID da disciplina que deseja remover: ")
                )

                remover_disciplina_turma(turma_id, disciplina_id)

            elif opcao == "19":
                print("\nAlunos cadastrados:")
                listar_alunos()
                aluno_id = int(input("\nID interno do aluno: "))

                print("\nTurmas cadastradas:")
                listar_turmas()
                turma_id = int(input("\nID da turma: "))

                ano_letivo = int(input("Ano letivo (ex.: 2026): "))

                cadastrar_matricula(
                    aluno_id,
                    turma_id,
                    ano_letivo
                )

            elif opcao == "20":
                listar_matriculas()

            elif opcao == "21":
                matricula_id = int(input("ID interno da matrícula: "))
                buscar_matricula(matricula_id)

            elif opcao == "22":
                matricula_id = int(
                    input("ID da matrícula que deseja atualizar: ")
                )

                print("\nAlunos cadastrados:")
                listar_alunos()
                aluno_id = int(input("\nNovo ID interno do aluno: "))

                print("\nTurmas cadastradas:")
                listar_turmas()
                turma_id = int(input("\nNovo ID da turma: "))

                ano_letivo = int(input("Novo ano letivo: "))

                atualizar_matricula(
                    matricula_id,
                    aluno_id,
                    turma_id,
                    ano_letivo
                )

            elif opcao == "23":
                matricula_id = int(
                    input("ID da matrícula que deseja excluir: ")
                )
                excluir_matricula(matricula_id)

            elif opcao == "24":
                print("\nMatrículas cadastradas:")
                listar_matriculas()

                matricula_id = int(
                    input("\nID interno da matrícula: ")
                )

                print("\nDisciplinas cadastradas:")
                listar_disciplinas()

                disciplina_id = int(input("\nID da disciplina: "))
                trimestre = int(input("Trimestre (1 a 4): "))

                print("\nDigite as notas de cada avaliação.")
                print("Se uma nota ainda não existir, pressione Enter.")

                p1_prova = ler_nota("P1 - Prova (0 a 6): ")
                p1_atividade = ler_nota("P1 - Atividade (0 a 4): ")
                p2_atividade1 = ler_nota("P2 - Atividade 1 (0 a 5): ")
                p2_atividade2 = ler_nota("P2 - Atividade 2 (0 a 5): ")
                p3_prova = ler_nota("P3 - Prova (0 a 10): ")

                lancar_notas(
                    matricula_id,
                    disciplina_id,
                    trimestre,
                    p1_prova,
                    p1_atividade,
                    p2_atividade1,
                    p2_atividade2,
                    p3_prova
                )

            elif opcao == "25":
                listar_matriculas()

                matricula_id = int(
                    input("\nID interno da matrícula para consultar o boletim: ")
                )

                consultar_boletim(matricula_id)

            elif opcao == "0":
                print("Encerrando o sistema. Até logo!")
                break

            else:
                print("Opção inválida. Escolha uma opção do menu.")

        except ValueError as erro:
            print(f"Entrada inválida: {erro}")

        except Exception as erro:
            print(f"Não foi possível realizar a operação: {erro}")


if __name__ == "__main__":
    menu()
