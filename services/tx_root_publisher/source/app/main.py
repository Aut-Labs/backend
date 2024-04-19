import json
import typing as t
import dataclasses

from web3 import Web3, HTTPProvider
import psycopg2 as pg
from psycopg2.extensions import connection as pg_conn
from eth_hash.auto import keccak as keccak256

from app.config import PgConfig, ContractsRelayerConfig
from app.utils import NodeMeta as MerkleTreeNodeMeta
from app.utils import build as build_merkle_tree


_read_interactions_sql = '''SELECT interaction_hash, chain_id, selector, tx_to 
FROM public.interactions;'''


# todo: move to common/misc/utils
def _get_connection() -> pg_conn:
    conn = pg.connect(host=PgConfig.POSTGRES_HOST,
                      databaset=PgConfig.POSTGRES_DB,
                      user=PgConfig.POSTGRES_USER)
    conn.autocommit = True
    return conn


# todo: move to common/misc/utils
@dataclasses.dataclass
class _EnforceTypeAnnotationsRuntime:
    def __post_init__(self):
        for name, field_type in self.__annotations__.items():
            if not isinstance(getattr(self, name), field_type):
                raise ValueError()


# todo: move to common/misc/utils
@dataclasses.dataclass
class Interaction(_EnforceTypeAnnotationsRuntime):
    interaction_hash: str
    chain_id: int
    selector: int
    tx_to: str



def _get_interactions() -> t.Iterator[dict]:
    with _get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(_read_interactions_sql)
            for row in cursor:
                yield row


# def _validate(row: dict[str, t.Any]) -> bool:
#     try:
#         Interaction(**row)
#     except ValueError:
#         return False
#     return True


class _MerkleTreeNode(MerkleTreeNodeMeta):
    hash_func: t.Callable[[str], bytes] = lambda x: keccak256(x.encode())
    delim: str = ":"


def _calc_new_merkle_root() -> bytes:
    values: list[str] = list(map(json.dumps, _get_interactions()))
    root = build_merkle_tree(_MerkleTreeNode, values)
    return root.hash_value


def push_new_merkle_root():
    next_root_hash: bytes = _calc_new_merkle_root()
    next_proof_hash: bytes = ...
    w3 = Web3(HTTPProvider(ContractsRelayerConfig.RPC_URL))
    InteractionDataset = w3.eth.contract(address=ContractsRelayerConfig.INTERACTION_DATASET_ADDR,
                                         abi=ContractsRelayerConfig.INTERACTION_DATASET_ABI["abi"])
    unsigned_tx = InteractionDataset.functions.updateRoot(next_root_hash,
                                                          next_proof_hash)
    w3.eth.account.sign_transaction(unsigned_tx, private_key=ContractsRelayerConfig.RELAYER_PK)


def main():
    push_new_merkle_root()
