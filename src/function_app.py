import logging
import azure.functions as func

app = func.FunctionApp()

# Importa triggers para registrar as functions no app
from triggers.extract_pedido import app as pedido
from triggers.extract_entrega import app as entrega
from triggers.extract_cliente import app as cliente

app.register_functions(pedido)
app.register_functions(entrega)
app.register_functions(cliente)