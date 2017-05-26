
import os
from flask import Flask, request, jsonify



app = Flask(__name__)



@app.route('/keyboard', methods=['GET'])
def Keyboard():

    dataSend = {
            "type" : "buttons",
            "buttons" : ["wa", "asdf"]
            }

    return jsonify(dataSend), 200, {'Content - Type' : 'application/json; charset=utf-8'}




if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)
