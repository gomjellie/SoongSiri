from flask import Flask
app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
SECRET_KEY='development key',
USERNAME='admin',
PASSWORD='default'
))

from app import views
