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
def message():
    try:
        jsn = request.get_json()
        viewLog("message", jsn)
        msg = APIAdmin.process("message", jsn).get_message()
        return jsonify(msg), 200
    except Exception as inst:
        traceback.print_exc()
        return process_fail(inst.__str__())


def process_fail(exception_str):
    user_key = request.get_json().get('user_key')
    msg = APIAdmin.process("fail", {'user_key': user_key, 'log': exception_str}).get_message()
    viewLog("fail", data=exception_str)
    return jsonify(msg)
