import os
from web3 import Web3, EthereumTesterProvider
from datetime import datetime, timedelta
import dataclasses
from eth_account import Account
from eth_account.messages import encode_defunct


@dataclasses.dataclass
class TConfig:
    signer: int
    private_key: int
    deadline: int
    accepted_domain: str


config = TConfig(**{['SECRET_KEY', 'TOKEN_DURATION', 'REFERENCE_ID']})


@dataclasses.dataclass
class TTokenRequest:
    sent_domain: str
    account: int
    timestamp: int
    signature: int


# def verify_token_request(self, Web3 w3, TConfig config, TTokenRequest request) -> bool:





# def main():
#     w3 = Web3(EthereumTesterProvider())
#     # w3.


# if __name__ == '__main__':
#     main()

