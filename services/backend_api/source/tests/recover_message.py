import sys
from web3.auto import w3
from eth_account.messages import encode_defunct


msg = encode_defunct(text=sys.argv[1])
sig = w3.to_bytes(hexstr=sys.argv[2])

print(w3.eth.account.recover_message(msg, signature=sig))
