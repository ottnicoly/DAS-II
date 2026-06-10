import azure.functions as func

from triggers.extract_categoria_produto import app as categoria_produto_bp
from triggers.extract_regiao import app as regiao_bp
from triggers.extract_transportadora import app as transportadora_bp
from triggers.extract_produto import app as produto_bp
from triggers.extract_representante import app as representante_bp
from triggers.extract_cliente import app as cliente_bp
from triggers.extract_estoque_saldo import app as estoque_saldo_bp
from triggers.extract_pedido import app as pedido_bp
from triggers.extract_pedido_item import app as pedido_item_bp
from triggers.extract_titulo_receber import app as titulo_receber_bp
from triggers.extract_entrega import app as entrega_bp
from triggers.extract_estoque_movimentacao import app as estoque_movimentacao_bp

app = func.FunctionApp()

app.register_functions(categoria_produto_bp)
app.register_functions(regiao_bp)
app.register_functions(transportadora_bp)
app.register_functions(produto_bp)
app.register_functions(representante_bp)
app.register_functions(cliente_bp)
app.register_functions(estoque_saldo_bp)
app.register_functions(pedido_bp)
app.register_functions(pedido_item_bp)
app.register_functions(titulo_receber_bp)
app.register_functions(entrega_bp)
app.register_functions(estoque_movimentacao_bp)