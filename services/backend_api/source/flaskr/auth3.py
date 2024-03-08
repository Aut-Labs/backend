import functools 

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask import request, jsonify
from werkzeug.http import HTTP_STATUS_CODES

from datetime import datetime, timedelta
from web3 import WEb3

bp = Blueprint('auth3', __name__, url_prefix='/auth3')

# class token_request_body:
#     def __init__(self, body):
#         self.__body = body
#     def 


# @bp.route('')


@bp.route('/token', methods=('POST'))
def process_token_request():
    # body = token_request_body(request.get_json(cache=False))
    timestamp = datetime.utcfromtimestamp(int(request.json["timestamp"]))

