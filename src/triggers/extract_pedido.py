import azure.functions as func
import logging
import os
#from orchestrators.etl_orchestrator import ETLOrchestrator

app = func.Blueprint()


@app.timer_trigger(schedule="0 0 6 * * *", arg_name="timer", run_on_startup=False)
def extract_pedido(timer: func.TimerRequest) -> None:
    sql_server = os.getenv("SQL_SERVER_SOURCE")
    sql_database = os.getenv("SQL_DATABASE_SOURCE")
    sql_user = os.getenv("SQL_USER_SOURCE")
    sql_password = os.getenv("SQL_PASSWORD_SOURCE")

    logging.info("Iniciando a extração de categoria_produto")
    logging.info(f"Conectando ao banco de dados SQL Server: {sql_server}")
    logging.info(f"Banco de dados: {sql_database}")
    logging.info("Extração de categoria_produto concluída com sucesso")
