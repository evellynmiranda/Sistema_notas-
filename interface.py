"""Interface gráfica para o sistema de notas escolares."""

import tkinter as tk
from contextlib import redirect_stdout
from datetime import date
from decimal import Decimal, InvalidOperation
from functools import partial
from io import StringIO
from tkinter import messagebox, ttk

import psycopg

import alunos
import disciplinas
import matriculas
import notas
import turma_disciplinas
import turmas
from database import conectar


def texto_obrigatorio(valor):
    if not valor:
        raise ValueError("Preencha todos os campos obrigatórios.")
    return valor


def data_opcional(valor):
    return date.fromisoformat(valor) if valor else None


def nota_opcional(valor):
    if not valor:
        return None
    nota = Decimal(valor.replace(",", "."))
    if not nota.is_finite():
        raise ValueError("Informe uma nota numérica finita.")
    return nota


class Formulario(ttk.Frame):
    def __init__(self, parent, campos):
        super().__init__(parent, padding=18)
        self.entradas = []
        self.columnconfigure(1, weight=1)
        for linha, (rotulo, converter) in enumerate(campos):
            ttk.Label(self, text=rotulo).grid(row=linha, column=0, sticky="w", pady=5)
            entrada = ttk.Entry(self)
            entrada.grid(row=linha, column=1, sticky="ew", padx=(16, 0))
            self.entradas.append((entrada, converter))

    def valores(self):
        return [converter(entrada.get().strip()) for entrada, converter in self.entradas]

    def preencher(self, valores=()):
        for entrada, _ in self.entradas:
            entrada.delete(0, tk.END)
        for (entrada, _), valor in zip(self.entradas, valores):
            if valor is not None:
                entrada.insert(0, str(valor))


class Sistema:
    def __init__(self, janela):
        self.janela = janela
        janela.title("Sistema de notas escolares")
        janela.geometry("920x680")
        janela.minsize(700, 580)

        estilo = ttk.Style(janela)
        estilo.theme_use("clam")
        estilo.configure("Title.TLabel", font=("TkDefaultFont", 18, "bold"))
        estilo.configure("Treeview", rowheight=27)
        estilo.configure("TNotebook.Tab", padding=(13, 8))

        painel = ttk.Frame(janela, padding=20)
        painel.pack(fill="both", expand=True)
        ttk.Label(painel, text="Sistema de notas escolares", style="Title.TLabel").pack(
            anchor="w", pady=(0, 14)
        )
        self.abas = ttk.Notebook(painel)
        self.abas.pack(fill="both", expand=True)
        self.status = tk.StringVar(value="Selecione uma aba para trabalhar.")
        ttk.Label(painel, textvariable=self.status, wraplength=650).pack(
            anchor="w", pady=(10, 0)
        )
        self.atualizacoes = {}
        self.criar_abas()
        self.abas.bind("<<NotebookTabChanged>>", self.aba_alterada)

    def criar_abas(self):
        texto = texto_obrigatorio
        self.cadastro(
            "Alunos",
            [("Nome", texto), ("Matrícula escolar", texto), ("Nascimento (AAAA-MM-DD)", data_opcional)],
            "SELECT id, nome, matricula, data_nascimento FROM alunos ORDER BY nome, id",
            alunos.cadastrar_aluno, alunos.atualizar_aluno, alunos.excluir_aluno,
        )
        self.cadastro(
            "Turmas",
            [("Nome", texto), ("Ano/série", texto), ("Turno", texto)],
            "SELECT id, nome, ano_serie, turno FROM turmas ORDER BY nome, id",
            turmas.cadastrar_turma, turmas.atualizar_turma, turmas.excluir_turma,
        )
        self.cadastro(
            "Disciplinas", [("Nome", texto)],
            "SELECT id, nome FROM disciplinas ORDER BY nome, id",
            disciplinas.cadastrar_disciplina, disciplinas.atualizar_disciplina,
            disciplinas.excluir_disciplina,
        )
        self.cadastro(
            "Matrículas",
            [("ID do aluno", int), ("ID da turma", int), ("Ano letivo", int)],
            """
            SELECT m.id, m.aluno_id, m.turma_id, m.ano_letivo, a.nome, t.nome
            FROM matriculas m
            JOIN alunos a ON a.id = m.aluno_id
            JOIN turmas t ON t.id = m.turma_id
            ORDER BY m.ano_letivo DESC, a.nome, m.id
            """,
            matriculas.cadastrar_matricula, matriculas.atualizar_matricula,
            matriculas.excluir_matricula, ["Aluno", "Turma"],
        )
        self.vinculos()
        self.aba_notas()

    def formulario(self, titulo, campos):
        formulario = Formulario(self.abas, campos)
        self.abas.add(formulario, text=titulo)
        return formulario

    def tabela(self, parent, colunas):
        quadro = ttk.Frame(parent)
        quadro.grid(columnspan=2, sticky="nsew", pady=(12, 0))
        parent.rowconfigure(quadro.grid_info()["row"], weight=1)
        tabela = ttk.Treeview(quadro, columns=tuple(colunas), show="headings",
                              selectmode="browse", height=8)
        for rotulo in colunas:
            tabela.heading(rotulo, text=rotulo)
            tabela.column(rotulo, width=90, minwidth=55)
        if colunas[0] == "ID":
            tabela.column("ID", width=55, stretch=False)
        barra = ttk.Scrollbar(quadro, command=tabela.yview)
        tabela.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        tabela.pack(side="left", fill="both", expand=True)
        return tabela

    def botoes(self, parent, acoes):
        quadro = ttk.Frame(parent)
        quadro.grid(columnspan=2, sticky="w", pady=(12, 0))
        for rotulo, acao in acoes:
            ttk.Button(quadro, text=rotulo, command=acao).pack(side="left", padx=(0, 8))

    def consultar(self, tabela, sql):
        with conectar() as conexao:
            registros = conexao.execute(sql).fetchall()
        tabela.delete(*tabela.get_children())
        for registro in registros:
            tabela.insert("", "end", values=["" if valor is None else valor for valor in registro])

    def executar(self, acao, atualizar=None):
        saida = StringIO()
        try:
            with redirect_stdout(saida):
                acao()
        except (ValueError, InvalidOperation, psycopg.Error) as erro:
            messagebox.showerror("Não foi possível concluir", str(erro), parent=self.janela)
            return
        self.status.set(saida.getvalue().strip() or "Dados atualizados.")
        if atualizar:
            self.executar(atualizar)
            if saida.getvalue().strip():
                self.status.set(saida.getvalue().strip())

    def aba_alterada(self, _evento):
        atualizar = self.atualizacoes.get(self.abas.select())
        if atualizar:
            self.executar(atualizar)

    def cadastro(self, titulo, campos, sql, cadastrar, atualizar, excluir, extras=()):
        formulario = self.formulario(titulo, campos)
        colunas = ["ID", *(rotulo for rotulo, _ in campos), *extras]

        def selecionar():
            itens = tabela.selection()
            if not itens:
                raise ValueError("Selecione um registro na tabela.")
            return tabela.item(itens[0], "values")

        def preencher(_evento):
            if tabela.selection():
                formulario.preencher(selecionar()[1:len(campos) + 1])

        def salvar():
            atualizar(int(selecionar()[0]), *formulario.valores())

        def apagar():
            identificador = int(selecionar()[0])
            if messagebox.askyesno("Excluir registro", f"Excluir o registro {identificador}?",
                                   parent=self.janela):
                self.executar(partial(excluir, identificador), recarregar)

        self.botoes(formulario, [
            ("Cadastrar", lambda: self.executar(lambda: cadastrar(*formulario.valores()), recarregar)),
            ("Salvar alterações", lambda: self.executar(salvar, recarregar)),
            ("Excluir", lambda: self.executar(apagar)),
            ("Atualizar lista", lambda: self.executar(recarregar)),
        ])
        tabela = self.tabela(formulario, colunas)
        recarregar = partial(self.consultar, tabela, sql)
        self.atualizacoes[str(formulario)] = recarregar
        tabela.bind("<<TreeviewSelect>>", preencher)

    def vinculos(self):
        formulario = self.formulario("Vínculos", [("ID da turma", int), ("ID da disciplina", int)])
        sql = """
            SELECT t.id, t.nome, d.id, d.nome
            FROM turma_disciplinas td
            JOIN turmas t ON t.id = td.turma_id
            JOIN disciplinas d ON d.id = td.disciplina_id
            ORDER BY t.nome, d.nome
        """

        def preencher(_evento):
            if tabela.selection():
                turma_id, _, disciplina_id, _ = tabela.item(tabela.selection()[0], "values")
                formulario.preencher((turma_id, disciplina_id))

        self.botoes(formulario, [
            ("Vincular", lambda: self.executar(
                lambda: turma_disciplinas.vincular_disciplina(*formulario.valores()), recarregar)),
            ("Remover vínculo", lambda: self.executar(
                lambda: turma_disciplinas.remover_disciplina_turma(*formulario.valores()), recarregar)),
            ("Atualizar lista", lambda: self.executar(recarregar)),
        ])
        tabela = self.tabela(formulario, ["ID da turma", "Turma", "ID da disciplina", "Disciplina"])
        recarregar = partial(self.consultar, tabela, sql)
        self.atualizacoes[str(formulario)] = recarregar
        tabela.bind("<<TreeviewSelect>>", preencher)

    def aba_notas(self):
        formulario = self.formulario("Notas", [
            ("ID da matrícula", int), ("ID da disciplina", int), ("Trimestre (1 a 4)", int),
            ("P1 — Prova (0 a 6)", nota_opcional), ("P1 — Atividade (0 a 4)", nota_opcional),
            ("P2 — Atividade 1 (0 a 5)", nota_opcional),
            ("P2 — Atividade 2 (0 a 5)", nota_opcional),
            ("P3 — Prova (0 a 10)", nota_opcional),
        ])
        self.botoes(formulario, [
            ("Salvar notas", lambda: self.executar(lambda: notas.lancar_notas(*formulario.valores()))),
        ])

        boletim = self.formulario("Boletim", [("ID da matrícula", int)])

        def consultar_boletim():
            matricula_id, = boletim.valores()
            saida = StringIO()
            with redirect_stdout(saida):
                notas.consultar_boletim(matricula_id)
            resultado.configure(state="normal")
            resultado.delete("1.0", tk.END)
            resultado.insert("1.0", saida.getvalue())
            resultado.configure(state="disabled")

        self.botoes(boletim, [("Consultar boletim", lambda: self.executar(consultar_boletim))])
        resultado = tk.Text(boletim, height=10, wrap="word", state="disabled", padx=12, pady=10)
        resultado.grid(columnspan=2, sticky="nsew", pady=(12, 0))
        boletim.rowconfigure(resultado.grid_info()["row"], weight=1)


if __name__ == "__main__":
    janela = tk.Tk()
    Sistema(janela)
    janela.mainloop()
