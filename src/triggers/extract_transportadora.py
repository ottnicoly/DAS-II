import azure.functions as func
from .etl_utils import copiar_tabela

app = func.Blueprint()


@app.timer_trigger(schedule="0 2 6 * * *", arg_name="timer", run_on_startup=False)
def extract_transportadora(timer: func.TimerRequest) -> None:
    copiar_tabela("transportadora")