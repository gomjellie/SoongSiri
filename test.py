#!/home/ubuntu/soongsiri/venv/bin/python

from flask import request, jsonify, Flask
app = Flask(__name__)
app.config.from_object(__name__)
import traceback
import json


@app.route('/')
def index():
    print("get_json")
    jsn = request.get_json()
    print(jsn)
    print("args")
    print(request.args)
    res = {'status': 'ok'}
    return jsonify(res), 200


@app.route('/api', methods=['POST', 'GET'])
def api():
    print("get_json")
    jsn = request.get_json()
    params = jsn['action']['params']
    print(params)
    date = params['date']
    place = params['place']

    json_file = open("res.json")
    data = json.load(json_file)
    json_file.close()

    res = {
        'version': "2.0",
	'template': {
	    'outputs': [
		{
		    'simpleImage': {
			'imageUrl': "https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
			'altText': "hello I'm Ryan"
		    },
		},
                {
                    'simpleText': {
                        "text": "스트링 포매팅 만드는중...\n" + json.dumps(data[date][place], ensure_ascii=False, indent=4),
                    },
                }
	    ],
            'quickReplies': [
                {
                    "label": "오늘의 식단",
                    "action": "block",
                    "messageText": "오늘의 식단",
                },
                {
                    "label": "내일의 식단",
                    "action": "block",
                    "messageText": "내일의 식단",
                },
            ],
	}
    };
    return jsonify(res), 200


@app.errorhandler(404)
def page_not_found(e):
    return process_fail('{} page_not_found'.format(request.url)), 404


def process_fail(exception_str):
    return jsonify("fail")

app.run(port=5000, host='0.0.0.0', debug=True)
