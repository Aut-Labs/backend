import os
import dataclasses
from moralis import evm_api
import typing as t
from psycopg2.extensions import connection as pg_conn


chainid_track_list = list(map(int, os.getenv("CHAINID_TRACK_LIST", "1,80001").split(",")))
api_key = os.getenv("API_KEY")


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


# <Moralis Native Tx>
# "hash": "0x057Ec652A4F150f7FF94f089A38008f49a0DF88e",
# "nonce": 326595425,
# "transaction_index": 25,
# "from_address": "0xd4a3BebD824189481FC45363602b83C9c7e9cbDf",
# "to_address": "0xa71db868318f0a0bae9411347cd4a6fa23d8d4ef",
# "from_address_label": "Binance 1",
# "to_address_label": "Binance 2",
# "value": 650000000000000000,
# "gas": 6721975,
# "gas_price": 20000000000,
# "input": "",
# "receipt_cumulative_gas_used": 1340925,
# "receipt_gas_used": 1340925,
# "receipt_contract_address": "0x1d6a4cf64b52f6c73f201839aded7379ce58059c",
# "receipt_root": "",
# "receipt_status": 1,
# "block_timestamp": "2021-04-02T10:07:54.000Z",
# "block_number": 12526958,
# "block_hash": "0x0372c302e3c52e8f2e15d155e2c545e6d802e479236564af052759253b20fd86",
# "internal_transactions": {
#     "transaction_hash": "0x057Ec652A4F150f7FF94f089A38008f49a0DF88e",
#     "block_number": 12526958,
#     "block_hash": "0x0372c302e3c52e8f2e15d155e2c545e6d802e479236564af052759253b20fd86",
#     "type": "CALL",
#     "from": "0xd4a3BebD824189481FC45363602b83C9c7e9cbDf",
#     "to": "0xa71db868318f0a0bae9411347cd4a6fa23d8d4ef",
#     "value": "650000000000000000",
#     "gas": "6721975",
#     "gas_used": "6721975",
#     "input": "0x",
#     "output": "0x"
# }


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
class Interaction:
    interaction_hash: str
    chain_id: int
    selector: int
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
        api_key=api_key,
        params=params,
    )
    return list(map(lambda x: MoralisNativeTransaction(**x), result))


def process_batch(
        interaction: Interaction,
        # txns: the same chain id
        txns: t.Iterable[MoralisNativeTransaction]
    ) -> t.Iterable[MoralisNativeTransaction]:
    def _process_one(interaction: Interaction) -> t.Callable[..., bool]:
        def _filter(tx: MoralisNativeTransaction) -> bool:
            return (interaction.tx_to == tx.to_address and 
                    len(tx.input) > 10 and 
                    hex(tx.input[:10]) == interaction.selector)
        return _filter
    yield from filter(_process_one(interaction), txns)
