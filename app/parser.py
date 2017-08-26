from bs4 import BeautifulSoup
import requests
from urllib import parse
import re
from collections import defaultdict
import datetime


class Singleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class FoodParser:
    def __init__(self):
        self.base_url = 'http://soongguri.com/menu/m_menujson.php'
        self.faculty_food = None
        self.pupil_food = None
        self.the_kitchen = None
        self.snack_corner = None
        self.food_court = None
        self.no_food_today = {
            '조식': {
                '메뉴': ['식단이 없습니다', '운영시간을 확인해 주세요']
            },
            '중식': {
                '메뉴': ['식단이 없습니다', '운영시간을 확인해 주세요']
            },
            '석식': {
                '메뉴': ['식단이 없습니다', '운영시간을 확인해 주세요']
            },
        }
        self.no_food_court_today = {
            '메뉴': ['식단이 없습니다', '운영시간을 확인해 주세요']
        }

    def refresh(self, day_of_week=None):
        """
        서버에 request를 보내서 식당 정보들을 갱신한다.
        인자로 fkey를 받는데 1은 월요일, 5는 금요일 이런식이다.
        fkey 인자를 생략하면 자동으로 오늘의 식단 가져옴
        fkey 가 7 이상으로 넘어가면 다음주식단을 가져옴
        fkey 가 음수로 되면 과거 데이터를 가져옴
        아쉬운점은 가격을 못가져온다
        가격은 http://soongguri.com/main.php?mkey=2&w=3&l=3&j=0 여기있음
        여기서 다 파싱하면 뒤질지도 모름
        내가 뒤지는게 아니라 프로그램이 뒤질거같음
        사이트가 규칙이 갑자기 바뀌면 뻗으니까 안전하게 base_url 지금쓰는거 쓰고
        base_url에서 가져온 메뉴검색 -> 부모의 다음 쌍둥이 -> day_of_week번째 항목에 있는 가격 가져오기 이런식으로 하는게
        그나마 안전하지 않을까
        :return: None
        """
        day_of_week = day_of_week or datetime.date.today().weekday()
        # date.weekday() 메소드는 월요일 0 일요일7인 반면 fkey는 월요일 1 일요일 0이다
        day_of_week = (day_of_week + 1) % 8
        res = requests.get(self.base_url, params={'fkey': day_of_week}, timeout=2)
        # res = requests.get(self.base_url, timeout=2)
        jsn = res.json()
        if not jsn:
            return
        self.pupil_food = jsn.get('학생식당')
        self.the_kitchen = jsn.get('THE KITCHEN')
        self.snack_corner = jsn.get('스넥코너')
        self.food_court = jsn.get('푸드코트')
        self.faculty_food = jsn.get('교직원식당')

    def get_food(self, place):
        if place == '학식':
            return self.get_pupil_food()
        elif place == '교식':
            return self.get_faculty_food()
        elif place == '푸드코트':
            return self.get_faculty_food()
        elif place == '기식':
            return self.get_dormitory_food()
        else:
            raise Exception('unexpected parameter place={}'.format(place))

    def get_faculty_food(self):
        """
        교식 메뉴
        :return: dict
        """
        ret_dict = defaultdict()
        if not self.faculty_food:
            return self.no_food_today

        for section in self.faculty_food:
            ret_dict.update({section: []})
            soup = BeautifulSoup(self.faculty_food[section], 'html.parser')
            t = ''
            if soup.find_all(['p']):
                for i in soup.find_all(['p']):
                    t += '\n' + i.text
            else:
                for i in soup.find_all(['div']):
                    t += '\n' + i.text
            exclude_english = re.compile('[^가-힣 ]+')

            res = exclude_english.sub('', ' '.join(t.split()))
            res = ' '.join(res.split())
            res = res.split(' ')

            ret_dict.update({section: {'메뉴': res}})
        return ret_dict

    def get_pupil_food(self):
        """
        exception 많이남(주말)
        :return: dict
        """
        ret_dict = defaultdict()
        if not self.pupil_food:
            return self.no_food_today

        for section in self.pupil_food:
            ret_dict.update({section: {'메뉴': []}})
            soup = BeautifulSoup(self.pupil_food[section], 'html.parser')
            t = ''
            if soup.find_all(['span']):
                for i in soup.find_all(['span']):
                    t += '\n' + i.text
            else:
                for i in soup.find_all(['div']):
                    t += '\n' + i.text

            exclude_english = re.compile('[^가-힣 ]+')

            res = exclude_english.sub('', ' '.join(t.split()))
            res = ' '.join(res.split())
            res = res.split(' ')

            ret_dict.update({section: {'메뉴': res}})
        return ret_dict

    def get_dormitory_food(self):
        dorm_url = 'http://ssudorm.ssu.ac.kr/SShostel/mall_main.php?viewform=B0001_foodboard_list&gyear={}&gmonth={}&gday={}'
        today = datetime.date.today()
        day_of_week = today.weekday()
        if day_of_week == 6:
            # 일요일에 다음주로 홈페이지가 넘어가버림
            yester_day = datetime.date.today() - datetime.timedelta(days=1)
            year = yester_day.year
            month = yester_day.month
            day = yester_day.day
        else:
            year = today.year
            month = today.month
            day = today.day
        res = requests.get(dorm_url.format(year, month, day), timeout=2)
        res.encoding = 'euc-kr'
        form = defaultdict()
        soup = BeautifulSoup(res.text, 'html.parser')
        parenthesis = re.compile(r"(\(.+)\)")
        table = soup.find_all('table', attrs={'class': 'boxstyle02'})[0]
        rows = table.findChildren(['tr'])
        day = 0  # 월화수목금 구분
        for row in rows[1:]:
            cells = row.findChildren('td')
            time = 0  # 조식 중식 석식 구분
            form.update({'월화수목금토일'[day]: {'조식': defaultdict(), '중식': defaultdict(), '석식': defaultdict()}})
            for cell in cells[:3]:  # 방학중에는 :3으로 슬라이싱 하고 학기중에는 :4로 슬라이싱 하면됨
                text = cell.text.strip()
                text = parenthesis.sub('', text)
                menu = text.split('\r\n')
                form['월화수목금토일'[day]][['조식', '중식', '석식'][time]]['메뉴'] = menu
                time += 1
            day += 1
        return form

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
            :return: dict
        """

        ret_dict = defaultdict()
        if not self.food_court:
            return self.no_food_court_today

        for section in self.food_court:
            ret_dict.update({section: []})
            soup = BeautifulSoup(self.food_court[section], 'html.parser')
            t = ''
            if soup.find_all(['span']) == []:
                for i in soup.find_all(['div']):
                    t += '\n' + i.text
            else:
                for i in soup.find_all(['span']):
                    t += '\n' + i.text

            hangul = re.compile('[^가-힣 0-9.]+')
            digit = re.compile(r"[(?P<num>(0-9.)*?)(?p<last>\s*)]+")

            s = hangul.sub('', ' '.join(t.split()))

            res = digit.sub('\g<0>\n', s).split('\n')
            res_list = []
            filter_item = ['일식', '퓨전', [], '', '직화']

            for i in res:
                if not any(j in i.split() for j in filter_item):
                    res_list.append(' '.join(i.split()))  # remove whitespace

            if res_list.count(''):
                res_list.remove('')

            ret_dict.update({section: list(set(res_list))})
        return ret_dict


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
            room['사용중인 좌석'] = int(room['전체 좌석'])-room['잔여 좌석']
            room['이용률'] = usage_percent
            cnt += 1

        return self.seat

subway_api = SubwayParser()
bus_api = BusParser()
lib_api = LibParser()
food_api = FoodParser()

