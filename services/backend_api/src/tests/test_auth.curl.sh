#!/usr/bin/env bash

readonly _port=5050
readonly _host="localhost"
readonly _version="v1"
readonly _api_base_url="http://${_host}:${_port}/api/${_version}"

function _eth_address_from_pk {
    printf "$1" | python -c 'from eth_account import Account; print((Account.from_key(input())).address)'
}

# readonly _der_file=ec.der
# function pem_file_from_pk {
#     local key="302e0201010420${1}a00706052b8104000a"
#     echo -n "${key}" | xxd -r -p | openssl ec -inform DER -outform PEM
# }
# pem_file_from_pk $_private_key > $_der_file 2>/dev/null

function main {
    local private_key="$(openssl rand -hex 32)"
    local eth_address="$(_eth_address_from_pk "0x${private_key}")"

    local json_fmt='{"message":%s,"signature":"%s"}'
    local json_msg_fmt='{"timestamp":%s,"signer":"%s","domain":"%s"}'
    local msg_text=$(printf $json_msg_fmt $(date +%s) "${eth_address}" $_host:$_port | jq -c .)
    local sig_text=$(python3 sign_message.py "${msg_text}" "0x${private_key}")
    local json=$(printf $json_fmt $msg_text $sig_text | jq -c .)

    echo ">> json body:"
    echo $json | jq .
    if [[ $eth_address == $(python3 recover_message.py $msg_text $sig_text) ]]; then
        echo ">> recovered address: ${eth_address}"
    fi

    local data=$(curl -s -XPOST "${_api_base_url}/auth/token" -H "Content-Type: application/json" -d $json)
    if [ $? -ne 0 ]; then
        echo "error!"
    fi
    echo ">> data: "
    echo $data | jq .

    local token=$(echo -n $data | jq -r .token)

    local payload=$(curl -s -XGET "${_api_base_url}/auth/token/payload" -H "X-Token: ${token}")
    if [ $? -ne 0 ]; then
        echo "error!"
    fi
    echo ">> payload:"
    echo $payload | jq .

    local json_fmt_inter='{"message":%s,"signature":"%s"}'
    local json_msg_fmt_inter='{"interaction_id":"%s","signer":"%s"}'
    local digest_inter=$(echo -n "abc" | openssl dgst -sha3-256 -hex | tail -c +18)
    local msg_text_inter=$(printf $json_msg_fmt_inter "0x${digest_inter}" $eth_address)
    local sig_text_inter=$(python3 sign_message.py $msg_text_inter "0x${private_key}")
    local json_inter=$(printf $json_fmt_inter $msg_text_inter $sig_text_inter)

    # echo $digest_inter
    # echo $msg_text_inter
    # echo $json_inter

    local data_inter=$(curl -s -XPOST "${_api_base_url}/interaction/approve" -H "Content-Type: application/json" -d $json_inter)
    echo ">> approve result:"
    echo $data_inter | jq .

    local approves=$(curl -s -XGET "${_api_base_url}/interaction/approve" -H "Content-Type: application/json" -H "X-Token: ${token}")
    echo ">> approves:"
    echo $approves | jq .
}

main $@
exit $?
