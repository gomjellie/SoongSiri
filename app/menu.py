from .parser import food_api
from .formatter import TreeFormatter
from collections import OrderedDict
import datetime
from app import hakusiku
from app import myLogger


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
            unordered_food = data[self.kor_name]
            self.foods = OrderedDict(sorted(unordered_food.items()))
            myLogger.viewLog("query", self.foods)

        else:
            try:
                food_api.refresh()
                unordered_food = food_api.get_food(self.kor_name)

            except Exception as inst:
                unordered_food = {
                    self.kor_name: [
                        inst.__str__(),
                        '파싱이 제대로 되지 않았습니다.',
                        '주말에는 메뉴가 없을 수 있습니다.'
                    ]
                }
            self.foods = OrderedDict(sorted(unordered_food.items()))

    def get_clean_dict(self):
        """
        remove rating, participant
        :return: dict
        """
        foods = self.foods
        for time in foods:
            if '참여자' in foods[time]:
                foods[time].pop('참여자')
            if '평점' in foods[time]:
                foods[time].pop('평점')
        return foods

    def get_dict(self):
        return self.foods

    def get_times(self):
        """
        ['조식', '중식', '중식2'] 이런식으로 리턴함
        :return: list
        """
        ret = []
        for time in self.foods:
            ret.append(time)
        return ret

    def get_string(self):
        dic = self.get_dict()
        dic.update(self.open_time)
        for time in dic:
            if '참여자' in dic[time]:
                dic[time].pop('참여자')
        t = TreeFormatter()
        t.prettify(dic)
        ret_string = t.prettified_str
        return ret_string

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

