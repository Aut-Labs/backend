import typing as t
import dataclasses

from moralis import evm_api

# from app.cfg import PgTxFetcherConfig


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


moralis_chain_by_chainid = {
    1: "eth",
    80001: "polygon"
}


def fetch_batch(tx_from: str, chain_id: int, block_from: int, step: int = 1) -> list[MoralisNativeTransaction]:
    params = {
        "chain": moralis_chain_by_chainid[chain_id],
        "order": "ASC",
        "address": tx_from,
        "from_block": block_from,
        "to_block": block_from + step
    }
    result = evm_api.transaction.get_wallet_transactions(
        api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6ImE1ZTgzNGFhLWM1NGUtNDQ2Zi04Y2U1LTM0NDFkNGQ4YjAyMCIsIm9yZ0lkIjoiMzg4Mzg1IiwidXNlcklkIjoiMzk5MDg5IiwidHlwZUlkIjoiYzA1NDY3NjEtYTVkZi00OGUyLWE4OWUtMWNjM2Q0NjA2MTFhIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3MTMzNzE2MDUsImV4cCI6NDg2OTEzMTYwNX0.W9-i2c5ai8ukWMRtM9XHmK9Pbvd83kjB1bWokFvdZHw",
        # api_key=PgTxFetcherConfig.MORALIS_API_KEY,
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
