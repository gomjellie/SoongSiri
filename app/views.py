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
        jsn = request.get_json()
        viewLog("message", jsn)
        message = APIAdmin.process("message", jsn).get_message()
        return jsonify(message), 200
    except Exception as inst:
        traceback.print_exc()
        return process_fail(inst.__str__(), jsn)


def process_fail(exception_str, jsn):
    user_key = jsn.get('user_key')
    message = APIAdmin.process("fail", {'user_key': user_key, 'log': exception_str}).get_message()
    viewLog("fail", data=exception_str)
    return jsonify(message)
