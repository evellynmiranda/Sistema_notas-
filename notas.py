from database import conectar


def lancar_notas(
    matricula_id, disciplina_id, trimestre, p1_prova, p1_atividade,
    p2_atividade1, p2_atividade2, p3_prova
):
    sql = """
        INSERT INTO notas_trimestrais (
            matricula_id, disciplina_id, trimestre,
            p1_prova, p1_atividade, p2_atividade1, p2_atividade2, p3_prova
        )
        SELECT m.id, td.disciplina_id, %s, %s, %s, %s, %s, %s
        FROM matriculas m
        JOIN turma_disciplinas td ON td.turma_id = m.turma_id
        WHERE m.id = %s AND td.disciplina_id = %s
        ON CONFLICT (matricula_id, disciplina_id, trimestre) DO UPDATE SET
            p1_prova = EXCLUDED.p1_prova,
            p1_atividade = EXCLUDED.p1_atividade,
            p2_atividade1 = EXCLUDED.p2_atividade1,
            p2_atividade2 = EXCLUDED.p2_atividade2,
            p3_prova = EXCLUDED.p3_prova
        RETURNING id;
    """
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (
                trimestre, p1_prova, p1_atividade, p2_atividade1,
                p2_atividade2, p3_prova, matricula_id, disciplina_id
            ))
            if cursor.fetchone() is None:
                raise ValueError(
                    "Informe uma matrícula existente e uma disciplina vinculada à turma."
                )

    print("Notas salvas com sucesso!")


def consultar_boletim(matricula_id):
    sql = """
        SELECT d.nome, n.trimestre, n.p1_prova, n.p1_atividade,
               n.p2_atividade1, n.p2_atividade2, n.p3_prova
        FROM notas_trimestrais n
        JOIN disciplinas d ON d.id = n.disciplina_id
        WHERE n.matricula_id = %s
        ORDER BY d.nome, n.trimestre;
    """
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (matricula_id,))
            registros = cursor.fetchall()

    if not registros:
        print("Nenhuma nota lançada para esta matrícula.")
        return

    print(f"Boletim da matrícula {matricula_id}")
    for disciplina, trimestre, *notas in registros:
        prova1, atividade1, atividade2, atividade3, prova3 = (
            "—" if nota is None else str(nota) for nota in notas
        )
        print(
            f"{disciplina} | Trimestre {trimestre} | "
            f"P1 prova: {prova1} | P1 atividade: {atividade1} | "
            f"P2 atividade 1: {atividade2} | P2 atividade 2: {atividade3} | "
            f"P3 prova: {prova3}"
        )
