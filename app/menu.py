from .parser import FoodParser
from .formatter import TreeFormatter
from collections import OrderedDict


class Menu:
    def __init__(self):
        self.foods = None
        self.prettified_str = ''

    def get_foods(self):
        return self.foods

    def get_dict(self):
        pass

    def get_string(self):
        # 메뉴마다 깔끔하게 딕셔너리를 string으로 바꾼다
        pass


class PupilMenu(Menu):
    def __init__(self):
        super().__init__()

    def set_pupil_foods(self):
        food_parser = FoodParser()
        try:
            food_parser.refresh()
            unordered_food = food_parser.get_pupil_food()
            unordered_food.update({
                '운영시간': [
                    '평일 :	10:30 ~ 14:00(중식)',
                    '주말 : '
                ]
            })
        except TypeError as inst:
            unordered_food = {'학생식당': [
                '오늘은 메뉴가 없습니다.',
                inst.__str__()
            ]}
        except Exception as inst:
            unordered_food = {'학생식당': [
                inst,
                '파싱이 제대로 되지 않았습니다.',
                '일요일에는 메뉴가 없어서 동작하지 않을 수 있습니다.'
            ]}
        self.foods = OrderedDict(sorted(unordered_food.items()))

    def get_dict(self):
        return self.foods

    def get_string(self):
        dic = self.get_dict()
        t = TreeFormatter()
        t.prettify(dic)
        ret_string = t.prettified_str
        return ret_string


class FacultyMenu(Menu):
    def __init__(self):
        super().__init__()

    def set_faculty_foods(self):
        food_parser = FoodParser()
        try:
            food_parser.refresh()
            unordered_food = food_parser.get_faculty_food()
            unordered_food.update({
                '운영시간': [
                    '평일 :	11:30 ~ 14:00(중식)',
                    '17:00 ~ 18:10(중식)',
                    '주말 :	11:30 ~ 14:00(중식)'
                ]})
        except TypeError as inst:
            unordered_food = {'교직원식당': [
                '오늘은 쉽니다.',
                inst.__str__()
            ]}
        except Exception as inst:
            unordered_food = {'교직원식당': [
                inst,
                '파싱이 제대로 되지 않았습니다.',
                '주말에는 메뉴가 없을 수 있습니다.'
            ]}
        self.foods = OrderedDict(sorted(unordered_food.items()))

    def get_dict(self):
        return self.foods

    def get_string(self):
        dic = self.get_dict()
        t = TreeFormatter()
        t.prettify(dic)
        ret_string = t.prettified_str

        return ret_string


class FoodCourtMenu(Menu):
    def __init__(self):
        super().__init__()

    def set_food_court_food(self):
        food_parser = FoodParser()
        try:
            food_parser.refresh()
            unordered_food = food_parser.get_food_court()
            unordered_food.update({
                '운영시간': [
                    '평일 :	11:00 ~ 15:00(중식)',
                    '주말 : 운영안함'
                ]
            })
        except TypeError as inst:
            unordered_food = {
                '푸드코트': [
                    '오늘은 쉽니다.',
                    inst.__str__()
                ]
            }
        except Exception as inst:
            unordered_food = {'교직원식당': [
                inst,
                '파싱이 제대로 되지 않았습니다.',
                '주말에는 메뉴가 없을 수 있습니다.'
            ]}
        self.foods = OrderedDict(sorted(unordered_food.items()))

    def get_dict(self):

        return self.foods

    def get_string(self):
        dic = self.get_dict()
        t = TreeFormatter()
        t.prettify(dic)
        ret_string = t.prettified_str

        return ret_string
