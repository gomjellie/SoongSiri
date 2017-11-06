import pymongo
import datetime

conn = pymongo.MongoClient()
food_db = conn.food_db
hakusiku = food_db.hakusiku

hakusiku.delete_one({'날짜': datetime.date.today()})

