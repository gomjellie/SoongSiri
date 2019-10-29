import pymongo
import datetime

conn = pymongo.MongoClient()
food_db = conn.food_db
hakusiku = food_db.hakusiku

hakusiku.delete_one({'날짜': datetime.date.today().__str__()})
tomorrow = datetime.date.today() + datetime.timedelta(days=1)
hakusiku.delete_one({'날짜': tomorrow.__str__()})
