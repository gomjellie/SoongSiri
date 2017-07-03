from .parser import FoodParser
from .formatter import TreeFormatter
from collections import OrderedDict


class Menu:
    def __init__(self):
        self.foods = None
        self.prettified_str = ''
        self.open_time = None

    def set_food(self):
        pass

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

    def set_food(self):
        food_parser = FoodParser()
        try:
            food_parser.refresh()
            unordered_food = food_parser.get_pupil_food()

        except Exception as inst:
            unordered_food = {
                '학생식당': [
                    inst.__str__(),
                    '파싱이 제대로 되지 않았습니다.',
                    '주말에는 메뉴가 없을 수 있습니다.'
                ]
            }
        self.foods = OrderedDict(sorted(unordered_food.items()))


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

    def set_food(self):
        food_parser = FoodParser()
        try:
            food_parser.refresh()
            unordered_food = food_parser.get_faculty_food()

        except Exception as inst:
            unordered_food = {
                '교직원식당': [
                    inst.__str__(),
                    '파싱이 제대로 되지 않았습니다.',
                    '주말에는 메뉴가 없을 수 있습니다.'
                ]
            }
        self.foods = OrderedDict(sorted(unordered_food.items()))


class FoodCourtMenu(Menu):
    def __init__(self):
        super().__init__()
        self.open_time = {
            '운영시간': [
                '평일 :   11:00 ~ 15:00(중식)',
                '주말 :   운영안함'
            ]
        }

    def set_food(self):
        food_parser = FoodParser()
        try:
            food_parser.refresh()
            unordered_food = food_parser.get_food_court()

        except Exception as inst:
            unordered_food = {
                '교직원식당': [
                    inst.__str__(),
                    '파싱이 제대로 되지 않았습니다.',
                    '주말에는 메뉴가 없을 수 있습니다.'
                ]
            }
        self.foods = OrderedDict(sorted(unordered_food.items()))
