import json
from flask import (
    Blueprint,
    request, jsonify, current_app
)
from datetime import datetime

import jwt
from web3 import Web3, EthereumTesterProvider
from eth_account.messages import encode_defunct

bp = Blueprint('authentication', __name__, url_prefix='/api/v1/auth')

_TIMESTAMP_CHECK_LATENCY = 60
_w3 = Web3(EthereumTesterProvider())

def _check_autid_token(address: str):
    # cache & request from autid subgraph
    ...
    return True


@bp.post('/token')
def process_token_issue_request():
    if not request.headers.get('Content-Type', 'application/json'):
        return jsonify(error="content-type header should be set to 'application/json'"), 400
    if not request.is_json:
         return jsonify(error="failed to parse json request body"), 400

    data = request.get_json()

    if not {'message', 'signature'}.issubset(data):
        return jsonify(error="request missing a required field"), 400
    message: dict = request.json['message']
    signature: str = str(request.json['signature'])

    if not {'timestamp', 'signer', 'domain'}.issubset(message):
        return jsonify(error="message missing a required field"), 400
    try:
        timestamp: int = int(message['timestamp'])
    except ValueError:
        return jsonify(error="timestamp should be integer"), 400
    signer: str = str(message['signer'])
    domain: str = str(message['domain'])

    signer_recovered = _w3.eth.account.recover_message(
        encode_defunct(text=json.dumps(message, separators=(',', ':'))),
        signature=Web3.to_bytes(hexstr=signature)
    )
    now = int(datetime.utcnow().timestamp())

    if domain != request.host:
        return jsonify(error='wrong domain'), 400
    if timestamp > now:
        return jsonify(error='timestamp is ahead'), 400
    if timestamp + _TIMESTAMP_CHECK_LATENCY < now:
        return jsonify(error='invalid timestamp'), 400
    if signer_recovered != signer:
        return jsonify(error='signer address missmatch'), 403
    if not _check_autid_token(signer):
        return jsonify(error='aut id token required'), 403
    
    token: str = \
        jwt.encode({'exp': timestamp + current_app.config["AUTH_TOKEN_DURATION"],
                    'iat': now,
                    'sub': signer,
                    'nbf': current_app.config["AUTH_BEGIN_TIMESTAMP"],
                    'iss': 'urn:autlabs',
                    'aud': 'urn:autlabs:autid:holder'},
                   current_app.config["SECRET_KEY"],
                   algorithm='ES256K')

    return jsonify(token=token), 200


@bp.get('/token/payload')
def process_token_check_request():
    token = request.headers.get('X-Token')
    if token is None:
        return jsonify(error="x-token header should be set"), 400

    try:
        payload = jwt.decode(
            token, 
            current_app.config["SECRET_KEY"],
            algorithms=['ES256K'],
            audience='urn:autlabs:autid:holder'
        )
    except jwt.PyJWTError as e:
        return jsonify(error=f"token validation failed with {repr(e)}"), 403

    return jsonify(payload=payload), 200