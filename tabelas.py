
from database import conectar


def criar_tabelas():
    comandos = [
        """
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            nome VARCHAR(150) NOT NULL,
            data_nascimento DATE,
            matricula VARCHAR(30) UNIQUE NOT NULL
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS turmas (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            nome VARCHAR(80) NOT NULL,
            ano_serie VARCHAR(30) NOT NULL,
            turno VARCHAR(20) NOT NULL
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS disciplinas (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            nome VARCHAR(100) UNIQUE NOT NULL
        );
        ALTER TABLE disciplinas
            ADD COLUMN IF NOT EXISTS descricao TEXT;
        """,

        """
        CREATE TABLE IF NOT EXISTS matriculas (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            aluno_id INTEGER NOT NULL REFERENCES alunos(id),
            turma_id INTEGER NOT NULL REFERENCES turmas(id),
            ano_letivo INTEGER NOT NULL,
            UNIQUE (aluno_id, ano_letivo)
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS turma_disciplinas (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            turma_id INTEGER NOT NULL REFERENCES turmas(id),
            disciplina_id INTEGER NOT NULL REFERENCES disciplinas(id),
            UNIQUE (turma_id, disciplina_id)
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS notas_trimestrais (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            matricula_id INTEGER NOT NULL REFERENCES matriculas(id),
            disciplina_id INTEGER NOT NULL REFERENCES disciplinas(id),
            trimestre INTEGER NOT NULL CHECK (trimestre BETWEEN 1 AND 4),

            p1_prova NUMERIC(4,2)
                CHECK (p1_prova BETWEEN 0 AND 6),
            p1_atividade NUMERIC(4,2)
                CHECK (p1_atividade BETWEEN 0 AND 4),

            p2_atividade1 NUMERIC(4,2)
                CHECK (p2_atividade1 BETWEEN 0 AND 5),
            p2_atividade2 NUMERIC(4,2)
                CHECK (p2_atividade2 BETWEEN 0 AND 5),

            p3_prova NUMERIC(4,2)
                CHECK (p3_prova BETWEEN 0 AND 10),

            UNIQUE (matricula_id, disciplina_id, trimestre)
        );
        """
    ]

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            for comando in comandos:
                cursor.execute(comando)

    print("Tabelas criadas com sucesso!")


if __name__ == "__main__":
    criar_tabelas()
