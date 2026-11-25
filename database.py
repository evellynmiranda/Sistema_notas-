"""Conexão com o PostgreSQL pelas variáveis de ambiente do libpq."""

import psycopg


def conectar():
    return psycopg.connect()
