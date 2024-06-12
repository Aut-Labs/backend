import psycopg2 as pg
from psycopg2.extensions import connection as pg_conn

from app.cfg import PostgresClientConfig


def _get_connection() -> pg_conn:
    conn = pg.connect(host=PostgresClientConfig.POSTGRES_HOST,
                      databaset=PostgresClientConfig.POSTGRES_DB,
                      user=PostgresClientConfig.POSTGRES_USER)
    conn.autocommit = True
    return conn


_select_interaction_by_hash_sql: str = """
select interaction_hash, chain_id, selector, tx_to 
from public.interaction 
    where 
        interaction_hash = '%x';"""


_select_max_block_id_for_holder_for_interaction_sql: str = """
select max(block_id)
from public.moralis_scan_checkpoints 
    where 
        interaction_hash = '%x' and 
        eth_address = '%x';"""


def load_interactions(interaction_hash: str, ):
    ...
