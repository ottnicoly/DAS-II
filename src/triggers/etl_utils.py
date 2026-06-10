import logging
from .conexao import get_source_conn, get_meu_conn

SCHEMA = "erp"
BATCH_SIZE = 1000


def nome_tabela(table_name: str) -> str:
    return f"[{SCHEMA}].[{table_name}]"


def get_columns(conn, table_name):
    sql = """
        SELECT c.name
        FROM sys.columns c
        INNER JOIN sys.tables t ON c.object_id = t.object_id
        INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE s.name = ?
          AND t.name = ?
          AND c.is_computed = 0
        ORDER BY c.column_id
    """

    cursor = conn.cursor()
    cursor.execute(sql, SCHEMA, table_name)

    columns = [row[0] for row in cursor.fetchall()]
    cursor.close()

    if not columns:
        raise Exception(f"Nenhuma coluna encontrada em {SCHEMA}.{table_name}")

    return columns


def get_pk_columns(conn, table_name):
    sql = """
        SELECT c.name
        FROM sys.indexes i
        INNER JOIN sys.index_columns ic 
            ON i.object_id = ic.object_id 
           AND i.index_id = ic.index_id
        INNER JOIN sys.columns c 
            ON ic.object_id = c.object_id 
           AND ic.column_id = c.column_id
        INNER JOIN sys.tables t 
            ON i.object_id = t.object_id
        INNER JOIN sys.schemas s 
            ON t.schema_id = s.schema_id
        WHERE i.is_primary_key = 1
          AND s.name = ?
          AND t.name = ?
        ORDER BY ic.key_ordinal
    """

    cursor = conn.cursor()
    cursor.execute(sql, SCHEMA, table_name)

    pk_columns = [row[0] for row in cursor.fetchall()]
    cursor.close()

    if not pk_columns:
        raise Exception(f"Nenhuma PK encontrada em {SCHEMA}.{table_name}")

    return pk_columns


def has_identity(conn, table_name):
    sql = """
        SELECT COUNT(1)
        FROM sys.columns c
        INNER JOIN sys.tables t ON c.object_id = t.object_id
        INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE s.name = ?
          AND t.name = ?
          AND c.is_identity = 1
    """

    cursor = conn.cursor()
    cursor.execute(sql, SCHEMA, table_name)

    result = cursor.fetchone()[0] > 0
    cursor.close()

    return result


def criar_merge_sql(table_name, columns, pk_columns):
    full_table = nome_tabela(table_name)

    source_select = ", ".join(f"? AS [{col}]" for col in columns)
    on_clause = " AND ".join(f"T.[{col}] = S.[{col}]" for col in pk_columns)

    update_columns = [col for col in columns if col not in pk_columns]

    insert_columns = ", ".join(f"[{col}]" for col in columns)
    insert_values = ", ".join(f"S.[{col}]" for col in columns)

    sql = f"""
        MERGE {full_table} AS T
        USING (
            SELECT {source_select}
        ) AS S
        ON {on_clause}
    """

    if update_columns:
        update_set = ", ".join(f"T.[{col}] = S.[{col}]" for col in update_columns)

        sql += f"""
        WHEN MATCHED THEN
            UPDATE SET {update_set}
        """

    sql += f"""
        WHEN NOT MATCHED BY TARGET THEN
            INSERT ({insert_columns})
            VALUES ({insert_values});
    """

    return sql


def copiar_tabela(table_name):
    source_conn = None
    target_conn = None

    try:
        logging.info(f"Iniciando carga da tabela {SCHEMA}.{table_name}")

        source_conn = get_source_conn()
        target_conn = get_meu_conn()

        columns = get_columns(target_conn, table_name)
        pk_columns = get_pk_columns(target_conn, table_name)
        identity = has_identity(target_conn, table_name)

        column_list = ", ".join(f"[{col}]" for col in columns)

        select_sql = f"""
            SELECT {column_list}
            FROM {nome_tabela(table_name)}
        """

        merge_sql = criar_merge_sql(table_name, columns, pk_columns)

        source_cursor = source_conn.cursor()
        target_cursor = target_conn.cursor()
        target_cursor.fast_executemany = True

        if identity:
            target_cursor.execute(f"SET IDENTITY_INSERT {nome_tabela(table_name)} ON")

        source_cursor.execute(select_sql)

        total = 0

        while True:
            rows = source_cursor.fetchmany(BATCH_SIZE)

            if not rows:
                break

            rows = [tuple(row) for row in rows]

            target_cursor.executemany(merge_sql, rows)
            target_conn.commit()

            total += len(rows)

            logging.info(f"{SCHEMA}.{table_name}: {total} registros enviados")

        if identity:
            target_cursor.execute(f"SET IDENTITY_INSERT {nome_tabela(table_name)} OFF")
            target_conn.commit()

        logging.info(f"Finalizado {SCHEMA}.{table_name}: {total} registros")

    except Exception as e:
        if target_conn:
            target_conn.rollback()

        logging.error(f"Erro ao copiar {SCHEMA}.{table_name}: {str(e)}")
        raise

    finally:
        try:
            if source_conn:
                source_conn.close()

            if target_conn:
                target_conn.close()
        except Exception:
            pass