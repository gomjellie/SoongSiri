#!/home/ubuntu/soongsiri/venv/bin/python

import ssubob
import datetime
import pprint
import json

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

print(json.dumps(data, ensure_ascii=False, indent=4))

