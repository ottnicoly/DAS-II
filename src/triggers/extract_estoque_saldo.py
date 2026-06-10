from etl_utils import copiar_tabela


def executar(source_conn, target_conn):
    copiar_tabela(source_conn, target_conn, "estoque_saldo")