from flask import request, jsonify
from app import app
from app.models import *

@app.route('/keyboard')
def keyboard():
    ret = {
	    "type" : "buttons",
	    "buttons" : ["선택 1", "선택 2", "선택 3"]
	    }
    return jsonify(ret)

@app.route('/message', methods=['POST'])
def Message():

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
