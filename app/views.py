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
        viewLog("message", request.json)
        message = APIAdmin.process("message", request.json).get_message()
        return jsonify(message), 200
    except:
        traceback.print_exc()
        return processFail()


    dataReceive = request.get_json()
    content = dataReceive['content']

    if content == u"시작하기":
        dataSend = {
                "message": {
                    "text": "아직 개발중이라 대답을 잘 못해도 이해해줘^^;"
                    }
                }
    elif content == u"도움말":
        dataSend = {
                "message": {
                    "text": "이제 곧 정식 버전이 출시될거야. 조금만 기다려~~~"
                    }
                }
    elif u"안녕" in content:
        dataSend = {
                "message": {
                    "text": "안녕~~ 반가워 ㅎㅎ"
                    }
                }
    else:
        dataSend = {
                "message": {
                    "text": "나랑 놀자 ㅋㅋㅋ"
                    }
                }

    return jsonify(dataSend)

def processFail():
    message = APIAdmin.process("fail").get_message()
    viewLog("fail")
    return jsonify(message)
