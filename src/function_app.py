import logging
import azure.functions as func

app = func.FunctionApp()

# Importa triggers para registrar as functions no app
from triggers.extract_categoria_produto import app as categoria_produto
from triggers.extract_cliente import app as cliente
from triggers.extract_entrega import app as entrega
from triggers.extract_estoque_movimentacao import app as estoque_movimentacao
from triggers.extract_estoque_saldo import app as estoque_saldo
from triggers.extract_pedido_item import app as pedido_item
from triggers.extract_pedido_pymssql import app as pedido_pymssql
from triggers.extract_pedido import app as pedido
from triggers.extract_produto import app as produto
from triggers.extract_regiao import app as regiao
from triggers.extract_representante import app as representante
from triggers.extract_titulo_receber import app as titulo_receber
from triggers.extract_transportadora import app as transportadora


app.register_functions(categoria_produto)
app.register_functions(cliente)
app.register_functions(entrega)
app.register_functions(estoque_movimentacao)
app.register_functions(estoque_saldo)
app.register_functions(pedido_item)
app.register_functions(pedido_pymssql)
app.register_functions(pedido)
app.register_functions(produto)
app.register_functions(regiao)
app.register_functions(representante)
app.register_functions(titulo_receber)
app.register_functions(transportadora)