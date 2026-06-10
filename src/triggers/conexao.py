import os
import pyodbc


def get_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise Exception(f"Variável de ambiente não configurada: {name}")

    return value


def criar_conexao(server: str, database: str, user: str, password: str):
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    return pyodbc.connect(conn_str)


def get_source_conn():
    return criar_conexao(
        get_env("SQL_SERVER_SOURCE"),
        get_env("SQL_DATABASE_SOURCE"),
        get_env("SQL_USER_SOURCE"),
        get_env("SQL_PASSWORD_SOURCE")
    )


def get_meu_conn():
    return criar_conexao(
        get_env("SQL_SERVER_MEU"),
        get_env("SQL_DATABASE_MEU"),
        get_env("SQL_USER_MEU"),
        get_env("SQL_PASSWORD_MEU")
    )