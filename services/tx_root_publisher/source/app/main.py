from app.config import PgConfig
from psycopg2.extensions import connection as pg_conn
import psycopg2 as pg


_sql = '''SELECT interaction FROM public.interactions
 
'''


def get_connection() -> pg_conn:
    conn = pg.connect(host=PgConfig.POSTGRES_HOST,
                    databaset=PgConfig.POSTGRES_DB,
                    user=PgConfig.POSTGRES_USER)
    conn.autocommit = True
    return conn


def get_interactions():
    ...
