from flask import jsonify
from app import app
from app.models import *

@app.route('/', methods=['GET','POST'])
def index():
    return jsonify({'res': 'this is response'})
