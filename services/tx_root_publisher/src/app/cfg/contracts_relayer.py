import os


class ContractsRelayer:
    RPC_URL: str = os.getenv("RPC_URL")
    INTERACTION_DATASET_ADDR: str = os.getenv("INTERACION_DATASET_ADDR")
    RELAYER_PK: str = os.getenv("RELAYER_PK")
    INTERACTION_DATASET_ABI: dict = {
        "abi": [{
            "type": "function",
            "name": "updateRoot",
            "inputs": [
                {
                    "name": "nextMerkleRoot",
                    "type": "bytes32",
                    "internalType": "bytes32"
                }, 
                {
                    "name": "nextProofsHash",
                    "type": "bytes32",
                    "internalType": "bytes32"
                }
            ],
            "outputs": [],
            "stateMutability": "nonpayable"
        }]
    }
