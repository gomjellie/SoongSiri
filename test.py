from flask import request, jsonify, Flask
app = Flask(__name__)
app.config.from_object(__name__)
import traceback


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
    print(jsn)
    print("args")
    print(request.args)
    res = {
        'version': "2.0",
	'template': {
	    'outputs': [
		{
		    'simpleImage': {
			'imageUrl': "https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
			'altText': "hello I'm Ryan"
			}
		    }
		]
	    }
	};
    return jsonify(res), 200


@app.errorhandler(404)
def page_not_found(e):
    return process_fail('{} page_not_found'.format(request.url)), 404


def process_fail(exception_str):
    return jsonify("fail")

app.run(port=5000, host='0.0.0.0', debug=True)
