from database import conectar


def cadastrar_turma(nome, ano_serie, turno):
    sql = """
        INSERT INTO turmas (nome, ano_serie, turno)
        VALUES (%s, %s, %s)
        RETURNING id;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (nome, ano_serie, turno))
            turma_id = cursor.fetchone()[0]

    print(f"Turma cadastrada com sucesso! ID: {turma_id}")


def listar_turmas():
    sql = """
        SELECT id, nome, ano_serie, turno
        FROM turmas
        ORDER BY nome;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            turmas = cursor.fetchall()

    if not turmas:
        print("Nenhuma turma cadastrada.")
        return

    for turma in turmas:
        print(
            f"ID: {turma[0]} | Nome: {turma[1]} | "
            f"Ano/Série: {turma[2]} | Turno: {turma[3]}"
        )


def buscar_turma(turma_id):
    sql = """
        SELECT id, nome, ano_serie, turno
        FROM turmas
        WHERE id = %s;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (turma_id,))
            turma = cursor.fetchone()

    if turma:
        print(
            f"ID: {turma[0]} | Nome: {turma[1]} | "
            f"Ano/Série: {turma[2]} | Turno: {turma[3]}"
        )
    else:
        print("Turma não encontrada.")


def atualizar_turma(turma_id, nome, ano_serie, turno):
    sql = """
        UPDATE turmas
        SET nome = %s,
            ano_serie = %s,
            turno = %s
        WHERE id = %s
        RETURNING id;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql, (nome, ano_serie, turno, turma_id)
            )
            resultado = cursor.fetchone()

    if resultado:
        print("Turma atualizada com sucesso!")
    else:
        print("Turma não encontrada.")


def excluir_turma(turma_id):
    sql = """
        DELETE FROM turmas
        WHERE id = %s
        RETURNING id;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (turma_id,))
            resultado = cursor.fetchone()

    if resultado:
        print("Turma excluída com sucesso!")
    else:
        print("Turma não encontrada.")