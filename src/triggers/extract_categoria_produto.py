import azure.functions as func
from .etl_utils import copiar_tabela

app = func.Blueprint()


@app.timer_trigger(schedule="0 0 6 * * *", arg_name="timer", run_on_startup=False)
def extract_categoria_produto(timer: func.TimerRequest) -> None:
    copiar_tabela("categoria_produto")