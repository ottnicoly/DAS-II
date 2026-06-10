import azure.functions as func
from .etl_utils import copiar_tabela

app = func.Blueprint()


@app.timer_trigger(schedule="0 6 6 * * *", arg_name="timer", run_on_startup=False)
def extract_estoque_saldo(timer: func.TimerRequest) -> None:
    copiar_tabela("estoque_saldo")