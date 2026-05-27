import azure.functions as func
import logging
import sqlite3
import os
import time

app = func.Blueprint()

@app.timer_trigger(schedule="0 0 6 * * *", arg_name="timer", run_on_startup=False)
def extract_pedido_sqllite(timer: func.TimerRequest) -> None:
    
    sql_server = os.getenv("SQL_SERVER_SOURCE")
    sql_database = os.getenv("SQL_DATABASE_SOURCE")
    sql_user = os.getenv("SQL_USER_SOURCE")
    sql_pass = os.getenv("SQL_PASSWORD_SOURCE")

    # Configura a string de conexão para o banco de dados SQL Server
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        inicio = time.perf_counter_ns()

        # Estabelece a conexão com o banco de dados SQLite
        conn = sqlite3.connect('erp_pedido.db')
        cursor = conn.cursor()
        
        query = "SELECT * FROM pedido LIMIT 5"

        # Executa a consulta SQL
        cursor.execute(query)

        # Busca todos os resultados da consulta
        rows = cursor.fetchall()
    
        logging.info(rows)           
        fim = time.perf_counter_ns()

        print(f"{fim - inicio} ns")
    except Exception as e:
        logging.error(f"Erro ao ler pedido do SQLite: {str(e)}")
        raise

    finally:
        if conn:
            conn.close()