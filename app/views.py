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
    except:
        traceback.print_exc()
        return processFail()


def processFail():
    message = APIAdmin.process("fail").get_message()
    viewLog("fail")
    return jsonify(message)
