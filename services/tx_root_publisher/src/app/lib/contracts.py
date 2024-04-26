import typing as t

import json
from web3 import Web3, HTTPProvider
from eth_hash.auto import keccak as keccak256

from app.cfg import ContractsRelayerConfig
from app.lib.merkle_tree import NodeMeta as MerkleTreeNodeMeta
from app.lib.merkle_tree import build as build_merkle_tree
from app.lib.database import get_interactions, Interaction


class _MerkleTreeNode(MerkleTreeNodeMeta):
    hash_func: t.Callable[[str], bytes] = lambda x: keccak256(x.encode())
    delim: str = ":"


def _calc_new_merkle_root() -> bytes:
    values: list[str] = list(map(json.dumps, get_interactions()))
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


__all__ = push_new_merkle_root,
