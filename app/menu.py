from .parser import food_api
from collections import OrderedDict
import datetime
from app import hakusiku
from app import myLogger
from .myLogger import logger_deco

class Menu:
    def __init__(self, open_time, kor_name):
        """
        :param open_time: '2017-07-03 이런 형태'
        :param kor_name: '학식, 교식, 푸드코트 중에 하나이다.'
        """
        self.foods = None
        self.open_time = open_time
        self.kor_name = kor_name

    def fetch_food(self):
        """
        draft of set_food func using hakusiku db
        :return: None
        """
        date = datetime.date.today().__str__()
        data = hakusiku.find_one({'날짜': date})
        if data:
            self.foods = data[self.kor_name]
            myLogger.viewLog("query", self.foods)

        else:
            try:
                food_api.refresh()
                foods = food_api.get_food(self.kor_name)

            except Exception as inst:
                foods = {
                    self.kor_name: [
                        inst.__str__(),
                        '파싱이 제대로 되지 않았습니다.',
                        '주말에는 메뉴가 없을 수 있습니다.'
                    ]
                }
            self.foods = foods

    def get_times(self):
        """
        ['조식', '중식', '중식2'] 이런식으로 리턴함
        :return: list
        """
        ret = []
        for time in self.foods:
            ret.append(time)
        return ret

    @staticmethod
    @logger_deco
    def format_to_string(menu, place):
        today = datetime.date.today().__str__()
        ret_string = '{} {}\n'.format(today, place)
        if place in ['학식', '교식']:
            for time in menu:
                ret_string += '\n{} (평점 {}/4.5)\n'.format(time, menu[time]['평점'])
                for dish in menu[time]['메뉴']:
                    ret_string += '*{}\n'.format(dish)
            return ret_string
        elif place == '푸드코트':
            for dish in menu['메뉴']:
                ret_string += '*{}\n'.format(dish)
            return ret_string
        else:
            raise Exception('undexpected place: {}'.format(place))

    def get_string(self):
        dic = self.foods
        place = self.kor_name

        return Menu.format_to_string(dic, place)

pupil_menu = Menu(open_time={
            '운영시간': [
                '평일 :   10:30 ~ 14:00(중식)',
                '주말 :   운영안함'
            ]
        }, kor_name='학식')

faculty_menu = Menu(open_time={
            '운영시간': [
                '평일 :   11:30 ~ 14:00(중식)',
                '평일 :   17:00 ~ 18:10(중식)',
                '주말 :   11:30 ~ 14:00(중식)'
            ]
        }, kor_name='교식')

food_court_menu = Menu(open_time={
            '운영시간': [
                '평일 :   11:00 ~ 15:00(중식)',
                '주말 :   운영안함'
            ]
        }, kor_name='푸드코트')

