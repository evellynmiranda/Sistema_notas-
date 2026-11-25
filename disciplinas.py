
from database import conectar


def cadastrar_disciplina(nome):
    sql = """
        INSERT INTO disciplinas (nome)
        VALUES (%s)
        RETURNING id;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (nome,))
            disciplina_id = cursor.fetchone()[0]

    print(f"Disciplina cadastrada com sucesso! ID: {disciplina_id}")


def listar_disciplinas():
    sql = """
        SELECT id, nome
        FROM disciplinas
        ORDER BY nome;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            disciplinas = cursor.fetchall()

    if not disciplinas:
        print("Nenhuma disciplina cadastrada.")
        return

    for disciplina in disciplinas:
        print(f"ID: {disciplina[0]} | Nome: {disciplina[1]}")


def buscar_disciplina(disciplina_id):
    sql = """
        SELECT id, nome
        FROM disciplinas
        WHERE id = %s;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (disciplina_id,))
            disciplina = cursor.fetchone()

    if disciplina:
        print(f"ID: {disciplina[0]} | Nome: {disciplina[1]}")
    else:
        print("Disciplina não encontrada.")


def atualizar_disciplina(disciplina_id, nome):
    sql = """
        UPDATE disciplinas
        SET nome = %s
        WHERE id = %s
        RETURNING id;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (nome, disciplina_id))
            resultado = cursor.fetchone()

    if resultado:
        print("Disciplina atualizada com sucesso!")
    else:
        print("Disciplina não encontrada.")


def excluir_disciplina(disciplina_id):
    sql = """
        DELETE FROM disciplinas
        WHERE id = %s
        RETURNING id;
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (disciplina_id,))
            resultado = cursor.fetchone()

    if resultado:
        print("Disciplina excluída com sucesso!")
    else:
        print("Disciplina não encontrada.")
