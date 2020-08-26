from flask import Flask
import pymongo

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))


_conn = pymongo.MongoClient()
_user = _conn.user
session = _user.session


from app import views, myLogger
myLogger.setLogger(app, 20)
