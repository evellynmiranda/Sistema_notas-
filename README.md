# Sistema de notas escolares

Aplicação em Python com interface gráfica e menu de terminal para cadastrar alunos, turmas, disciplinas e
matrículas, lançar notas por trimestre e consultar o boletim.

## Como executar

1. No Ubuntu, instale o suporte à interface gráfica e aos ambientes virtuais.

   ```bash
   sudo apt install python3-tk python3-venv
   ```

   Na pasta do projeto, crie um ambiente virtual e instale a dependência.

   ```bash
   python3 -m venv .venv
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

3. Crie as tabelas e abra a janela do sistema.

   ```bash
   python tabelas.py
   python interface.py
   ```

Na janela, selecione uma linha da tabela para editar ou excluir um cadastro.
Os identificadores usados nos formulários aparecem nas tabelas. Antes de
lançar notas, vincule a disciplina à turma e matricule o aluno. Salvar novamente
para a mesma matrícula, disciplina e trimestre substitui as notas daquele
trimestre. Campos em branco ficam sem nota. A aba **Boletim** mostra as
avaliações registradas por disciplina e trimestre.

Para abrir o menu de terminal, execute `python main.py` com o ambiente virtual
ativado.
