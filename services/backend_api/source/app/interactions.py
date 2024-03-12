import json
from flask import (
    Blueprint,
    request, jsonify, current_app
)
from eth_account.messages import encode_defunct

from web3 import Web3, EthereumTesterProvider
from eth_account.messages import encode_defunct

bp = Blueprint('interactions', __name__, url_prefix='/api/v1/interaction')

_TIMESTAMP_CHECK_LATENCY = 60
_w3 = Web3(EthereumTesterProvider())


@bp.post('/consent')
def process_interaction_consent():
    data = request.get_json()

    if not {'message', 'signature'}.issubset(data):
        return 400, jsonify(error="")
    message = request.json['message']
    signature = request.json['signature']

    if not 'id' in message:
        return 400, jsonify(error="")
    interaction_id = message['id']

    message['counterparty'] = "urn:autlabs:autid:repository"
    signer_recovered = _w3.eth.account.recover_message(
        encode_defunct(text=json.dumps(message)),
        signature=Web3.to_bytes(hexstr=signature)
    )
