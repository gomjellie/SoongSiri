from bs4 import BeautifulSoup
import requests
import urllib

class Parser:
    def __init__(self):
        self.base_url = None

    def refresh(self):
        pass



class Singleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class FoodParser(Parser):
    def __init__(self):
        self.base_url = 'http://soongguri.com/menu/m_menujson.php'
        self.faculty_food = None
        self.pupil_food = None
        self.the_kitchen = None
        self.snack_corner = None
        self.food_court = None

    def refresh(self):
        """
        서버에 request를 보내서 식당 정보들을 갱신한다.
        인자로 fkey를 받는데 1은 월요일, 5는 금요일 이런식이다.
        :return: None
        """
        res = requests.get(self.base_url)
        jsn = res.json()
        self.pupil_food = jsn.get('학생식당')
        self.the_kitchen = jsn.get('THE KITCHEN')
        self.snack_corner = jsn.get('스넥코너')
        self.food_court = jsn.get('푸드코트')
        self.faculty_food = jsn.get('교직원식당')

    def get_faculty_food(self):
        ret_dict = {}
        for section in self.faculty_food:
            ret_dict.update({section: []})
            soup = BeautifulSoup(self.faculty_food[section], 'html.parser')
            ret_dict[section].append(soup.text)

        ret_dict.pop('조식') # 조식은 항상 조식 : 조식 이런 의미없는 데이터만 있음
        #교식이 점심부터 시작하는것 같다.

        return ret_dict

    def get_pupil_food(self):
        ret_dict = {}
        for section in self.pupil_food:
            ret_dict.update({section: []})
            soup = BeautifulSoup(self.pupil_food[section], 'html.parser')
            ret_dict[section].append(soup.text)
        return ret_dict

    def get_the_kitchen(self):
        """
        TODO: 정규표현식 이용해서 메뉴 가격 깔끔하게 나누기
        :return: dict
        """
        ret_dict = {}
        for section in self.the_kitchen:
            ret_dict.update({section: []})
            soup = BeautifulSoup(self.the_kitchen[section], 'html.parser')
            ret_dict[section].append(soup.text)
        return ret_dict

    def get_snack_corner(self):
        """
            TODO: 정규표현식 이용해서 메뉴 가격 깔끔하게 나누기
            :return: dict
        """
        ret_dict = {}
        for section in self.snack_corner:
            ret_dict.update({section: []})
            soup = BeautifulSoup(self.snack_corner[section], 'html.parser')
            ret_dict[section].append(soup.text)
        return ret_dict

    def get_food_court(self):
        """
            TODO: 정규표현식 이용해서 메뉴 가격 깔끔하게 나누기
            :return: dict
        """
        ret_dict = {}
        for section in self.food_court:
            ret_dict.update({section: []})
            soup = BeautifulSoup(self.food_court[section], 'html.parser')
            ret_dict[section].append(soup.text)
        return ret_dict


class SubwayParser(metaclass=Singleton):
    """

    """
    station_name_url = 'http://m.bus.go.kr/mBus/subway/getStatnByNm.bms'
    arrival_info_url = 'http://m.bus.go.kr/mBus/subway/getArvlByInfo.bms'

    def get_station_stat(self, station_name):
        station_name = urllib.parse.quote(station_name.replace('역', ''))
        # 숭실대입구역 -> 숭실대입구 로 변환해야 검색됨
        # 문제점 역삼역 같은경우 역삼역 -> 삼 으로 변환됨...!
        res = requests.get(subway_api.station_name_url + '?' + 'statnNm=' + station_name.replace('%', '%25'))
        jsn = res.json()

        if res.json().get('resultList') is None:
            return '그런역 없습니다 다른이름으로 검색하세요'
        subway_id = jsn.get('resultList')[0].get('subwayId')
        statn_id = jsn.get('resultList')[0].get('statnId')

        res = requests.get(subway_api.arrival_info_url + '?' +
                           'subwayId=' + subway_id + '&statnId=' + statn_id)
        jsn = res.json()
        """
        result of print(jsn) is
        {'resultList': [{'bTrainKind': '0', 'statnId': '1007000738', 'subwayList': '1007',
        'statnSn': '30', 'curstatnsn': '0', 'cStatnNm': '남성방면', 'arvlMsg': ' ', 'statnList':
        '1007000738', 'bStatnId': '30', 'bArvlTm': '60', 'updnLine': '상행', 'trnsitCo': '1',
        'subwayHeading': '오른쪽', 'statnNm': '숭실대입구(살피재)', 'trainLineNm': '도봉산행 -
        남성방면', 'gpsX': '126.95364613852064', 'arvlCd': '2', 'subwayId': '1007', 'trainLine':
        '0', 'acdntCn': ' ', 'bStatnNm': '도봉산행', 'delayTime': '0', 'arvlMsg2':
        '숭실대입구(살피재) 출발', 'bArvlDt': '60', 'bTrainNo': '7118', 'bStatnSn': '30', 'trainCd':
        '2', 'gpsY': '37.49636243455655', 'arvlMsg3': '숭실대입구(살피재)'}, {'bTrainKind': '0',
        'statnId': '1007000738', 'subwayList': '1007', 'statnSn': '30', 'curstatnsn': '2',
        'cStatnNm': '남성방면', 'arvlMsg': ' ', 'statnList': '1007000738', 'bStatnId': '32',
        'bArvlTm': '240', 'updnLine': '상행', 'trnsitCo': '1', 'subwayHeading': '오른쪽', 'statnNm':
            '숭실대입구(살피재)', 'trainLineNm': '장암행 - 남성방면', 'gpsX': '126.95364613852064',
            'arvlCd': '99', 'subwayId': '1007', 'trainLine': '0', 'acdntCn': ' ', 'bStatnNm':
            '장암행', 'delayTime': '0', 'arvlMsg2': '4분 후 (장승배기)', 'bArvlDt': '240',
            'bTrainNo': '7120', 'bStatnSn': '32', 'trainCd': '1', 'gpsY': '37.49636243455655',
            'arvlMsg3': '장승배기'}, {'bTrainKind': '0', 'statnId': '1007000738', 'subwayList':
            '1007', 'statnSn': '30', 'curstatnsn': '1', 'cStatnNm': '상도방면', 'arvlMsg': ' ',
            'statnList': '1007000738', 'bStatnId': '29', 'bArvlTm': '120', 'updnLine': '하행',
            'trnsitCo': '1', 'subwayHeading': '왼쪽', 'statnNm': '숭실대입구(살피재)',
            'trainLineNm': '온수행 - 상도방면', 'gpsX': '126.95364613852064', 'arvlCd': '3',
            'subwayId': '1007', 'trainLine': '1', 'acdntCn': ' ', 'bStatnNm': '온수행', 'delayTime':
            '0', 'arvlMsg2': '전역 출발', 'bArvlDt': '120', 'bTrainNo': '7123', 'bStatnSn': '29',
            'trainCd': '2', 'gpsY': '37.49636243455655', 'arvlMsg3': '남성'}, {'bTrainKind': '0',
            'statnId': '1007000738', 'subwayList': '1007', 'statnSn': '30', 'curstatnsn': '2',
            'cStatnNm': '상도방면', 'arvlMsg': ' ', 'statnList': '1007000738', 'bStatnId': '28',
            'bArvlTm': '300', 'updnLine': '하행', 'trnsitCo': '1', 'subwayHeading': '왼쪽',
            'statnNm': '숭실대입구(살피재)', 'trainLineNm': '부평구청행 - 상도방면', 'gpsX':
            '126.95364613852064', 'arvlCd': '99', 'subwayId': '1007', 'trainLine': '1', 'acdntCn': '
            ', 'bStatnNm': '부평구청행', 'delayTime': '0', 'arvlMsg2': '5분 후 (총신대입구(이수))',
            'bArvlDt': '300', 'bTrainNo': '7125', 'bStatnSn': '28', 'trainCd': '1', 'gpsY':
            '37.49636243455655', 'arvlMsg3': '총신대입구(이수)'}], 'error': {'errorCode': '0000',
            'errorMessage': '성공'}, 'resultList2': [{'x': '195901.37022', 'statnId': '1007000738',
            'zipNo': '156035', 'subwayId': '1007', 'subwayList': '1007:1007000738,', 'telNo':
            '02-6311-7381', 'statnTid': '1007000737', 'adres': '서울특별시 동작구 상도5동178-1',
            'fxNum': ' ', 'statnFnm': '상도', 'statnTnm': '남성', 'statnFid': '1007000739',
            'statnNmEng': 'Soongsil Univ.', 'operPblinstt': '도시철도', 'y': '444107.01879',
            'subwayNm': '7호선', 'trnsitCo': '1', 'statnNm': '숭실대입구'}]}
        """

        ret = jsn.get('resultList2')[0].get('statnNm') + '\n'

        if jsn.get('resultList') is None:
            return '곧 수정하겠습니다 아직 이부분은 왜안되는지 이유를 모르겠네요'
        for j in range(len(jsn.get('resultList'))):
            ret += '-----------------------\n|'
            ret += jsn.get('resultList')[j].get('trainLineNm') + '\n| '
            ret += jsn.get('resultList')[j].get('arvlMsg2') + '\n|'
            # for k in jsn.get('resultList')[j].keys():
            #	print(k, jsn.get('resultList')[j].get(k))
            # print('-------------------')

        return ret + '-----------------------'


subway_api = SubwayParser()
