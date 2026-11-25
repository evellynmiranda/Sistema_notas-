# Sistema de notas escolares

Aplicação de terminal em Python para cadastrar alunos, turmas, disciplinas e
matrículas, lançar notas por trimestre e consultar o boletim.

## Como executar

1. Crie um ambiente virtual e instale a dependência.

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

2. Com o PostgreSQL em execução, crie um banco de dados e configure a conexão
   com as variáveis do PostgreSQL. Substitua os valores de exemplo pelos do
   seu ambiente.

   ```bash
   export PGHOST=localhost PGPORT=5432 PGDATABASE=sistema_notas PGUSER=seu_usuario
   ```

   Se o servidor exigir senha, configure um arquivo `~/.pgpass` com permissão
   0600 ou forneça `PGPASSWORD` pelo ambiente.

3. Crie as tabelas e abra o menu.

   ```bash
   python tabelas.py
   python main.py
   ```

Antes de lançar notas, vincule a disciplina à turma (opção 16) e matricule o
aluno (opção 19). Na opção 24, lançar novamente para a mesma matrícula,
disciplina e trimestre substitui as notas daquele trimestre. Campos em branco
ficam sem nota. A opção 25 mostra as avaliações registradas por disciplina e
trimestre.
