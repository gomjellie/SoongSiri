import ssubob
from bs4 import BeautifulSoup
import requests
from urllib import parse


class Singleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class FoodParser:
    def __init__(self):
        pass

    def refresh(self, date=None):
        ssubob.refresh(date)

    def get_food(self, place):
        return ssubob.get(place)


class SubwayParser(metaclass=Singleton):
    def __init__(self):
        self.station_name_url = 'http://m.bus.go.kr/mBus/subway/getStatnByNm.bms'
        self.arrival_info_url = 'http://m.bus.go.kr/mBus/subway/getArvlByInfo.bms'

    def get_station_stat(self, station_name):
        station_name = parse.quote(station_name.replace('역', ''))
        # 숭실대입구역 -> 숭실대입구 로 변환해야 검색됨
        # 문제점 역삼역 같은경우 역삼역 -> 삼 으로 변환됨...!
        station_url = self.station_name_url + '?' + 'statnNm=' + station_name.replace('%', '%25')
        res = requests.get(station_url, timeout=1.5)
        jsn = res.json()

        if res.json().get('resultList') is None:
            return '그런역 없습니다 다른이름으로 검색하세요'
        subway_id = jsn.get('resultList')[0].get('subwayId')
        statn_id = jsn.get('resultList')[0].get('statnId')

        res = requests.get(self.arrival_info_url + '?' +
                           'subwayId=' + subway_id + '&statnId=' + statn_id, timeout=1.5)
        jsn = res.json()

        ret = jsn.get('resultList2')[0].get('statnNm') + '\n'

        if jsn.get('resultList') is None:
            return '결과가 없습니다.'
        for j in range(len(jsn.get('resultList'))):
            ret += '────────────\n'
            ret += jsn.get('resultList')[j].get('trainLineNm') + '\n'
            ret += jsn.get('resultList')[j].get('arvlMsg2') + '\n'
        return ret + '────────────'


class BusParser(metaclass=Singleton):
    """
    ex: http://bus.go.kr/xmlRequest/getStationByUid.jsp?strBusNumber=13157'
    """

    def __init__(self):
        self.url = 'http://bus.go.kr/xmlRequest/getStationByUid.jsp'

    def get_station_stat(self, station_number):
        res = requests.get(self.url, dict(strBusNumber=station_number), timeout=1.5)
        soup = BeautifulSoup(res.text, 'html.parser')
        ret = ''

        for bus_name, left_time_1, left_time_2 in zip(soup.select('rtnm'),
                                                      soup.select('arrmsg1'), soup.select('arrmsg2')):
            ret += "────────────\nBus:{0:<8}\n{1:<10}\n{2:<13}\n".format(
                bus_name.string, left_time_1.string, left_time_2.string)
        return ret + '────────────'


class LibParser(metaclass=Singleton):
    def __init__(self):
        self.url = 'http://203.253.28.47/seat/domian5.asp'
        self.seat = {
            '1 열람실': {
                '전체 좌석': 428,
                '잔여 좌석': None,
                '사용중인 좌석': None,
                '이용률': None
            },
            '2 열람실': {
                '전체 좌석': 100,
                '잔여 좌석': None,
                '사용중인 좌석': None,
                '이용률': None
            },
            '3 열람실': {
                '전체 좌석': 117,
                '잔여 좌석': None,
                '사용중인 좌석': None,
                '이용률': None
            },
            '4 열람실': {
                '전체 좌석': 172,
                '잔여 좌석': None,
                '사용중인 좌석': None,
                '이용률': None
            }
        }

    def get_lib_stat(self):
        """
        :return: dict
        """
        r = requests.get(self.url, timeout=1.5)
        soup = BeautifulSoup(r.text, 'html.parser')
        cnt = 1
        for i in soup.find_all('tr')[3:]:
            rest = i.find_all(attrs={'color': 'blue'})[1].getText()
            usage_percent = i.find_all(attrs={'color': 'blue'})[2].getText()
            room = self.seat['{} 열람실'.format(cnt)]
            room['잔여 좌석'] = int(rest)
            room['사용중인 좌석'] = int(room['전체 좌석']) - int(room['잔여 좌석'])
            room['이용률'] = usage_percent
            cnt += 1

        return self.seat


subway_api = SubwayParser()
bus_api = BusParser()
lib_api = LibParser()
food_api = FoodParser()

