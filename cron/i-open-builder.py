import ssubob
import datetime
import pprint

tomorrow = datetime.date.today() + datetime.timedelta(days=1)
ssubob.refresh(tomorrow)

data = {
    '내일': {
        '교식': ssubob.get('교식'),
        '학식': ssubob.get('학식'),
    },
}

ssubob.refresh(datetime.date.today())

data['오늘'] = {
    '교식': ssubob.get('교식'),
    '학식': ssubob.get('학식'),
}

print(data)

