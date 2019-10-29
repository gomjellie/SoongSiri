import pymongo


_conn = pymongo.MongoClient()
_user = _conn.user
session = _user.session

cursor = session.find()

while cursor:
    session.remove(cursor.next())

