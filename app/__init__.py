from flask import Flask
from collections import defaultdict

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

session = defaultdict()

from app import views, myLogger
myLogger.setLogger(app, 20)
