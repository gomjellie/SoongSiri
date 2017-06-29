from flask import request, jsonify
from .managers import APIAdmin
from app import app
from .myLogger import viewLog
import traceback


@app.route('/keyboard')
def keyboard():
    home_message = APIAdmin.process("home").get_message()
    return jsonify(home_message), 200


@app.route('/message', methods=['POST'])
def Message():
    try:
        viewLog("message", request.get_json())
        message = APIAdmin.process("message", request.get_json()).get_message()
        return jsonify(message), 200
    except Exception as inst:
        traceback.print_exc()
        return process_fail(inst)


def process_fail(exception_str):
    message = APIAdmin.process("fail", {'content': 'fail', 'log': exception_str}).get_message()
    viewLog("fail")
    return jsonify(message)
