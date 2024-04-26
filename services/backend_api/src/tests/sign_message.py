import sys
from web3.auto import w3
from eth_account.messages import encode_defunct

msg = encode_defunct(text=sys.argv[1])
pk = w3.to_bytes(hexstr=sys.argv[2])

sig = w3.eth.account.sign_message(msg, private_key=pk)
print(w3.to_hex(sig.signature))
