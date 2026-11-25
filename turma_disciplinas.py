from database import conectar


def vincular_disciplina(turma_id, disciplina_id):
    sql = """
        INSERT INTO turma_disciplinas (turma_id, disciplina_id)
        VALUES (%s, %s)
        RETURNING id;
    """
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (turma_id, disciplina_id))
            vinculo_id = cursor.fetchone()[0]

    print(f"Disciplina vinculada à turma com sucesso! ID do vínculo: {vinculo_id}")


def listar_disciplinas_turma(turma_id):
    sql = """
        SELECT d.id, d.nome
        FROM turma_disciplinas td
        JOIN disciplinas d ON d.id = td.disciplina_id
        WHERE td.turma_id = %s
        ORDER BY d.nome;
    """
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (turma_id,))
            disciplinas = cursor.fetchall()

    if not disciplinas:
        print("Essa turma não possui disciplinas vinculadas.")
        return

    for disciplina_id, nome in disciplinas:
        print(f"ID: {disciplina_id} | Nome: {nome}")


def remover_disciplina_turma(turma_id, disciplina_id):
    sql = """
        DELETE FROM turma_disciplinas
        WHERE turma_id = %s AND disciplina_id = %s
        RETURNING id;
    """
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (turma_id, disciplina_id))
            resultado = cursor.fetchone()

    if resultado:
        print("Disciplina removida da turma com sucesso!")
    else:
        print("Vínculo não encontrado.")
