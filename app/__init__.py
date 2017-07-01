from flask import Flask
import pymongo

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

conn = pymongo.MongoClient()
food_db = conn.food_db

hakusiku = food_db.hakusiku

from app.scheduler import menu_scheduler
menu_scheduler.start()

from app import views, myLogger
myLogger.setLogger(app, 20)
