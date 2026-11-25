
from database import conectar


def cadastrar_aluno(nome, matricula, data_nascimento=None):
    sql = """
        INSERT INTO alunos (nome, matricula, data_nascimento)
        VALUES (%s, %s, %s)
        RETURNING id;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (nome, matricula, data_nascimento))
            aluno_id = cursor.fetchone()[0]

    print(f"Aluno cadastrado com sucesso! ID: {aluno_id}")


def listar_alunos():
    sql = """
        SELECT id, nome, matricula, data_nascimento
        FROM alunos
        ORDER BY nome;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            alunos = cursor.fetchall()

    if not alunos:
        print("Nenhum aluno cadastrado.")
        return

    for aluno in alunos:
        print(
            f"ID: {aluno[0]} | "
            f"Nome: {aluno[1]} | "
            f"Matrícula: {aluno[2]} | "
            f"Nascimento: {aluno[3]}"
        )


def buscar_aluno(aluno_id):
    sql = """
        SELECT id, nome, matricula, data_nascimento
        FROM alunos
        WHERE id = %s;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (aluno_id,))
            aluno = cursor.fetchone()

    if aluno:
        print(
            f"ID: {aluno[0]} | Nome: {aluno[1]} | "
            f"Matrícula: {aluno[2]} | Nascimento: {aluno[3]}"
        )
    else:
        print("Aluno não encontrado.")


def atualizar_aluno(aluno_id, nome, matricula, data_nascimento=None):
    sql = """
        UPDATE alunos
        SET nome = %s,
            matricula = %s,
            data_nascimento = %s
        WHERE id = %s
        RETURNING id;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (nome, matricula, data_nascimento, aluno_id)
            )
            resultado = cursor.fetchone()

    if resultado:
        print("Aluno atualizado com sucesso!")
    else:
        print("Aluno não encontrado.")


def excluir_aluno(aluno_id):
    sql = """
        DELETE FROM alunos
        WHERE id = %s
        RETURNING id;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (aluno_id,))
            resultado = cursor.fetchone()

    if resultado:
        print("Aluno excluído com sucesso!")
    else:
        print("Aluno não encontrado.")
