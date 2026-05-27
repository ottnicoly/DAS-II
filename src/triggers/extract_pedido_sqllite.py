from pathlib import Path
import azure.functions as func
import logging
import sqlite3
import time

app = func.Blueprint()

@app.timer_trigger(schedule="0 0 6 * * *", arg_name="timer", run_on_startup=False)
def extract_pedido_sqllite(timer: func.TimerRequest) -> None:
    conn = None

    try:
        inicio = time.perf_counter_ns()

        db_path = Path(__file__).resolve().parent / "erp_pedido.db"

        if not db_path.exists():
            raise FileNotFoundError(f"Banco SQLite não encontrado em: {db_path}")

        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM pedido LIMIT 5")
        rows = cursor.fetchall()

        logging.info(rows)

        fim = time.perf_counter_ns()
        logging.info(f"Tempo execução: {fim - inicio} ns")

    except Exception as e:
        logging.error(f"Erro ao ler pedido do SQLite: {str(e)}")
        raise

    finally:
        if conn is not None:
            conn.close()