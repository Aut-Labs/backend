import typing as t
import dataclasses

from moralis import evm_api
import psycopg2 as pg
from psycopg2.extensions import connection as pg_conn

from app.config import PgConfig, PgTxFetcherConfig


# todo: move to common/misc/utils
# pylint: disable=duplicate-code
def get_connection() -> pg_conn:
    conn = pg.connect(host=PgConfig.POSTGRES_HOST,
                      databaset=PgConfig.POSTGRES_DB,
                      user=PgConfig.POSTGRES_USER)
    conn.autocommit = True
    return conn


moralis_chain_by_chainid = {
    1: "eth",
    80001: "polygon"
}


select_interaction_by_hash_sql: str = """
select interaction_hash, chain_id, selector, tx_to 
from public.interaction 
    where 
        interaction_hash = '%x';"""


select_max_block_id_for_holder_for_interaction_sql: str = """
select max(block_id)
from public.moralis_scan_checkpoints 
    where 
        interaction_hash = '%x' and 
        eth_address = '%x';"""


@dataclasses.dataclass
class MoralisNativeTransaction:
    block_timestamp: str
    block_hash: str
    block_number: int
    input: str
    from_address: str
    to_address: str
    value: int
    receipt_status: int
    tx_hash: str



@dataclasses.dataclass
class InteractionDefinition:
    chain_id: int
    selector: str
    tx_to: str



def fetch_batch(tx_from: str, chain_id: int, block_from: int, step: int = 1) -> list[MoralisNativeTransaction]:
    params = {
        "chain": moralis_chain_by_chainid[chain_id],
        "order": "ASC",
        "address": tx_from,
        "from_block": block_from,
        "to_block": block_from + step
    }
    result = evm_api.transaction.get_wallet_transactions(
        api_key=PgTxFetcherConfig.MORALIS_API_KEY,
        params=params,
    )['result']
    return list(map(lambda x: MoralisNativeTransaction(**{
        'block_timestamp': x['block_timestamp'],
        'block_hash': x['block_hash'], 
        'block_number': x['block_number'],
        'input': x['input'],
        'from_address': x['from_address'],
        'to_address': x['to_address'], 
        'value': x['value'],
        'receipt_status': x['receipt_status'],
        'tx_hash': x['hash']
    }), result))


def process_batch(
        interaction: InteractionDefinition,
        # txns: the same chain id
        txns: t.Iterable[MoralisNativeTransaction]
    ) -> t.Iterable[MoralisNativeTransaction]:
    def _process_one(interaction: InteractionDefinition) -> t.Callable[..., bool]:
        def _filter(tx: MoralisNativeTransaction) -> bool:
            return (interaction.tx_to == tx.to_address and 
                    len(tx.input) > 10 and 
                    tx.input[:10] == interaction.selector)
        return _filter
    yield from filter(_process_one(interaction), txns)


def test_process_batch():
    batch = fetch_batch(
        tx_from="0x49753299f25CA4117226Ac680D8b4eB56864b431",
        chain_id=1,
        block_from=19701531,
        step=1
    )
    interaction = InteractionDefinition(chain_id=1, selector="0xa9059cbb", tx_to="0xdac17f958d2ee523a2206206994597c13d831ec7")
    processed = list(process_batch(interaction, batch))
    print(processed)


__all__ = (
    process_batch,
    fetch_batch,
    select_interaction_by_hash_sql,
    select_max_block_id_for_holder_for_interaction_sql,
    MoralisNativeTransaction,
    InteractionDefinition
)
