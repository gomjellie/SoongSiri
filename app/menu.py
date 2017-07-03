from .parser import food_api
from .formatter import TreeFormatter
from collections import OrderedDict
import datetime
from app import hakusiku
from app import myLogger


class Menu:
    def __init__(self):
        self.foods = None
        self.prettified_str = ''
        self.open_time = '2017-07-03 이런 형태'
        self.kor_name = '학식, 교식, 푸드코트 중에 하나이다.'

    def set_food(self):
        """
        draft of set_food func using hakusiku db
        :return: None
        """
        date = datetime.datetime.now().date().__str__()
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

    def get_dict(self):
        self.foods.update(self.open_time)
        return self.foods

    def get_string(self):
        dic = self.get_dict()
        t = TreeFormatter()
        t.prettify(dic)
        ret_string = t.prettified_str
        return ret_string


class PupilMenu(Menu):
    def __init__(self):
        super().__init__()
        self.open_time = {
            '운영시간': [
                '평일 :	10:30 ~ 14:00(중식)',
                '주말 :  운영안함'
            ]
        }
        self.kor_name = '학식'


class FacultyMenu(Menu):
    def __init__(self):
        super().__init__()
        self.open_time = {
            '운영시간': [
                '평일 :   11:30 ~ 14:00(중식)',
                '평일 :   17:00 ~ 18:10(중식)',
                '주말 :   11:30 ~ 14:00(중식)'
            ]
        }
        self.kor_name = '교식'


class FoodCourtMenu(Menu):
    def __init__(self):
        super().__init__()
        self.open_time = {
            '운영시간': [
                '평일 :   11:00 ~ 15:00(중식)',
                '주말 :   운영안함'
            ]
        }
        self.kor_name = '푸드코트'
