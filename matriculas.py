
from database import conectar


def cadastrar_matricula(aluno_id, turma_id, ano_letivo):
    sql = """
        INSERT INTO matriculas (aluno_id, turma_id, ano_letivo)
        VALUES (%s, %s, %s)
        RETURNING id;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql, (aluno_id, turma_id, ano_letivo)
            )
            matricula_id = cursor.fetchone()[0]

    print(
        f"Matrícula cadastrada com sucesso! ID: {matricula_id}"
    )


def listar_matriculas():
    sql = """
        SELECT
            m.id,
            a.nome,
            a.matricula,
            t.nome,
            m.ano_letivo
        FROM matriculas m
        JOIN alunos a ON a.id = m.aluno_id
        JOIN turmas t ON t.id = m.turma_id
        ORDER BY m.ano_letivo DESC, a.nome;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            matriculas = cursor.fetchall()

    if not matriculas:
        print("Nenhuma matrícula cadastrada.")
        return

    for matricula in matriculas:
        print(
            f"ID: {matricula[0]} | "
            f"Aluno: {matricula[1]} | "
            f"Matrícula escolar: {matricula[2]} | "
            f"Turma: {matricula[3]} | "
            f"Ano letivo: {matricula[4]}"
        )


def buscar_matricula(matricula_id):
    sql = """
        SELECT
            m.id,
            a.nome,
            a.matricula,
            t.nome,
            m.ano_letivo
        FROM matriculas m
        JOIN alunos a ON a.id = m.aluno_id
        JOIN turmas t ON t.id = m.turma_id
        WHERE m.id = %s;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (matricula_id,))
            matricula = cursor.fetchone()

    if matricula:
        print(
            f"ID da matrícula: {matricula[0]} | "
            f"Aluno: {matricula[1]} | "
            f"Matrícula escolar: {matricula[2]} | "
            f"Turma: {matricula[3]} | "
            f"Ano letivo: {matricula[4]}"
        )
    else:
        print("Matrícula não encontrada.")


def atualizar_matricula(matricula_id, aluno_id, turma_id, ano_letivo):
    sql = """
        UPDATE matriculas
        SET aluno_id = %s,
            turma_id = %s,
            ano_letivo = %s
        WHERE id = %s
        RETURNING id;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (aluno_id, turma_id, ano_letivo, matricula_id)
            )
            resultado = cursor.fetchone()

    if resultado:
        print("Matrícula atualizada com sucesso!")
    else:
        print("Matrícula não encontrada.")


def excluir_matricula(matricula_id):
    sql = """
        DELETE FROM matriculas
        WHERE id = %s
        RETURNING id;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (matricula_id,))
            resultado = cursor.fetchone()

    if resultado:
        print("Matrícula excluída com sucesso!")
    else:
        print("Matrícula não encontrada.")
