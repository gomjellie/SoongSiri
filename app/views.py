from flask import request, jsonify
from .managers import APIAdmin
from app import app
from .myLogger import viewLog
import traceback


@app.route('/')
def index():
    return '', 200


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
    except Exception as e:
        traceback.print_exc()
        return process_fail(traceback.format_exc())


@app.route('/friend', methods=['POST'])
def add_friend():
    viewLog('add', request.get_json())
    msg = APIAdmin.process('etc').get_message()
    return jsonify(msg), 200


@app.route("/friend/<user_key>", methods=["DELETE"])
def block_friend(user_key):
    viewLog('block', user_key)
    msg = APIAdmin.process('etc').get_message()
    return jsonify(msg), 200


@app.route("/refresh", methods=["GET"])
def refresh():
    msg = APIAdmin.process("scheduler").get_message()
    return jsonify(msg), 200

@app.route("/refresh_tomorrow", methods=["GET"])
def refresh_tomorrow():
    msg = APIAdmin.process("refresh_tomorrow").get_message()
    return jsonify(msg), 200


@app.route("/chat_room/<user_key>", methods=["DELETE"])
def exit_chat_room(user_key):
    viewLog('exit', user_key)
    msg = APIAdmin.process('etc').get_message()
    return jsonify(msg), 200


@app.errorhandler(404)
def page_not_found(e):
    return process_fail('{} page_not_found'.format(request.url)), 404


def process_fail(exception_str):
    jsn = request.get_json() or {'user_key': 'not_user'}
    user_key = jsn.get('user_key')
    msg = APIAdmin.process("fail", {'user_key': user_key, 'log': exception_str}).get_message()
    viewLog("fail", data=exception_str)
    return jsonify(msg)

