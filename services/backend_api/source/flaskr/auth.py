import json
from flask import (
    Blueprint,
    request, jsonify, flash, g, current_app
)
from datetime import datetime, timedelta
import jwt

from web3 import Web3, EthereumTesterProvider
from eth_account.messages import encode_defunct

_TIMESTAMP_CHECK_LATENCY = 60

bp = Blueprint('authentication', __name__, url_prefix='/auth/token')

_w3 = Web3(EthereumTesterProvider())

def _check_autid_token(address: str):
    # cache & request from autid subgraph
    ...
    return True

@bp.post('/issue')
def process_token_issue_request():
    message = request.json['message']
    signature = request.json['signature']

    timestamp: int = int(datetime.utcfromtimestamp(message['timestamp']))
    signer: str = message['signer']
    domain: str = message['domain']
    
    signer_recovered = _w3.eth.account.recover_message(
        encode_defunct(text=json.dumps(message)),
        signature=Web3.to_bytes(hexstr=signature)
    )

    now = datetime.utcnow()

    if domain != current_app.config.domain:
        return 400, jsonify(error='wrong domain')
    if timestamp > now.timestamp:
        return 400, jsonify(error='timestamp is ahead')
    if timestamp + _TIMESTAMP_CHECK_LATENCY < now:
        return 400, jsonify(error='invalid timestamp')
    if signer_recovered != signer:
        return 403, jsonify(error='signer address missmatch')
    if not _check_autid_token(signer):
        return 403, jsonify(error='aut id token required')
    
    token = \
        jwt.encode({'exp': timestamp + timedelta(current_app.config.auth_token_duration),
                    'iat': timestamp,
                    'sub': signer,
                    'nbf': current_app.config.auth_begin_timestamp,
                    'iss': 'urn:autlabs:autid',
                    'aud': 'urn:autlabs:autid:holder',
                    'address': signer},
                   current_app.config.secret_key,
                   algorithm='ES256K')

    return 200, jsonify(token=token)

@bp.get('/check')
def process_token_check_request():
    token = request.headers.get('X-Token')

    if token is None:
        return 403, jsonify(error="'X-Token' header missing")

    try:
        payload = jwt.decode(token, current_app.config.secret_key, algorithms=['ES256K'])
    except jwt.PyJWTError:
        return 403, jsonify(error="wrong token")

    return 200, jsonify(address=payload.get('address'))
