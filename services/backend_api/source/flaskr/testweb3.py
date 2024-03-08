import os
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3, EthereumTesterProvider
from web3.middleware import construct_sign_and_send_raw_middleware
from eth_account.messages import encode_defunct

w3 = Web3(EthereumTesterProvider())

private_key = os.environ.get("PRIVATE_KEY")
print(private_key)
# input()
assert private_key is not None, "You must set PRIVATE_KEY environment variable"
assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"

account: LocalAccount = Account.from_key(private_key)
w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))

print(f"Your hot wallet address is {account.address}")

# Now you can use web3.eth.send_transaction(), Contract.functions.xxx.transact() functions
# with your local private key through middleware and you no longer get the error
# "ValueError: The method eth_sendTransaction does not exist/is not available

# private_key_bytes = encode_defunct(hexstr=private_key)
# print(private_key_bytes)
# print(private_key_bytes.body)
# print(Web3.to_hex(private_key_bytes))


data = {"a":1,"b":"0x22"}
data = str(data)
print(data)
# input()
sig_msg = w3.eth.account.sign_message(encode_defunct(Web3.to_bytes(text=data)), private_key=private_key)
print(sig_msg)
print(w3.eth.account.recover_message(encode_defunct(Web3.to_bytes(text=data+',')), signature=sig_msg.signature))