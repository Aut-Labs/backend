import typing as t
import dataclasses

import psycopg2 as pg
from psycopg2.extensions import connection as pg_conn

from app.cfg import PostgresClientConfig


_read_interactions_sql = '''SELECT 
    interaction_hash,
    chain_id, 
    selector, 
    tx_to 
FROM public.interactions;'''


@dataclasses.dataclass
class _EnforceTypeAnnotationsRuntime:
    def __post_init__(self):
        for name, field_type in self.__annotations__.items():
            if not isinstance(getattr(self, name), field_type):
                raise ValueError()


def _get_connection() -> pg_conn:
    conn = pg.connect(host=PostgresClientConfig.POSTGRES_HOST,
                      databaset=PostgresClientConfig.POSTGRES_DB,
                      user=PostgresClientConfig.POSTGRES_USER)
    conn.autocommit = True
    return conn


@dataclasses.dataclass
class Interaction(_EnforceTypeAnnotationsRuntime):
    interaction_hash: str
    chain_id: int
    selector: int
    tx_to: str


def get_interactions() -> t.Iterator[dict]:
    with _get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(_read_interactions_sql)
            for row in cursor:
                yield Interaction(interaction_hash=row[0],
                                  chain_id=row[1],
                                  selector=row[2],
                                  tx_to=row[3])


__all__ = (get_interactions, Interaction)
