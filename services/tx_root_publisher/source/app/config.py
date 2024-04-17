import os


class ContractsRelayerConfig:
    INTERACTION_DATASET_ADDR = os.getenv("INTERACION_DATASET_ADDR")
    RELAYER_PK: str = os.getenv("RELAYER_PK")
    DATASET_ABI: dict = {
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
