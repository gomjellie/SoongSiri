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

from app.scheduler import menu_scheduler
menu_scheduler.start()
menu_scheduler.fetch_save_menu()    # test 용으로 앱 시작하면 한번 패치함

from app import views, myLogger
myLogger.setLogger(app, 20)
