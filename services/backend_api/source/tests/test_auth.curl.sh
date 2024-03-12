#!/usr/bin/env bash

readonly _port=5000
readonly _host="localhost"
readonly _version="v1"
readonly _api_base_url="http://${_host}:${_port}/api/${_version}"

function eth_address_from_pk {
    printf "$1" | python -c 'from eth_account import Account; print((Account.from_key(input())).address)'
}

readonly _private_key="$(openssl rand -hex 32)"
readonly _eth_address="$(eth_address_from_pk "0x${_private_key}")"

# readonly _der_file=ec.der
# function pem_file_from_pk {
#     local key="302e0201010420${1}a00706052b8104000a"
#     echo -n "${key}" | xxd -r -p | openssl ec -inform DER -outform PEM
# }
# pem_file_from_pk $_private_key > $_der_file 2>/dev/null

readonly _json_fmt='{"message":%s,"signature":"%s"}'
readonly _message_fmt='{"timestamp":%s,"signer":"%s","domain":"%s"}'
readonly _msg_text=$(printf $_message_fmt $(date +%s) "${_eth_address}" localhost:5000 | jq -c .)
readonly _sig_text=$(python3 sign_message.py "${_msg_text}" "0x${_private_key}")
readonly _json=$(printf $_json_fmt $_msg_text $_sig_text)

echo ">> json body:"
echo $_json | jq .
if [[ $_eth_address == $(python3 recover_message.py $_msg_text $_sig_text) ]]; then
    echo ">> recovered address: ${_eth_address}"
fi

readonly _data=$(curl -s -XPOST "${_api_base_url}/auth/token" -H "Content-Type: application/json" -d $_json)
if [ $? -ne 0 ]; then
    echo "error!"
fi
echo ">> data: "
echo $_data | jq .

readonly _token=$(echo -n $_data | jq -r .token)

readonly _payload=$(curl -s -XGET "${_api_base_url}/auth/token/payload" -H "X-Token: ${_token}")
if [ $? -ne 0 ]; then
    echo "error!"
fi
echo ">> payload:"
echo $_payload | jq .
