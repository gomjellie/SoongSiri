from .parser import FoodParser
import re
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

    def prettify(self, d, indent=0):
        if isinstance(d, dict):
            for key, value in d.items():
                self.prettified_str += '\n├─' * (indent + 1) + str(key)
                if isinstance(value, dict) or isinstance(value, list):
                    self.prettify(value, indent + 1)
                else:
                    self.prettified_str += '\n│  ├' + '─' * (indent + 1) + str(value)
        elif isinstance(d, list):
            for item in d:
                if isinstance(item, dict) or isinstance(item, list):
                    self.prettify(item, indent + 1)
                else:
                    if item == d[-1]:
                        self.prettified_str += '\n│  └' + '─' * (indent) + str(item)
                    else:
                        self.prettified_str += '\n│  ├' + '─' * (indent) + str(item)
        else:
            return Exception


class PupilMenu(Menu):
    def __init__(self):
        super().__init__()

    def set_pupil_foods(self):
        food_parser = FoodParser()
        try:
            food_parser.refresh()
            unordered_food = food_parser.get_pupil_food()
        except TypeError:
            unordered_food = {'학생식당': '오늘은 메뉴가 없습니다.'}
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
        self.prettify(dic)
        ret_string = self.prettified_str
        return ret_string


class FacultyMenu(Menu):
    def __init__(self):
        super().__init__()

    def set_faculty_foods(self):
        food_parser = FoodParser()
        try:
            food_parser.refresh()
            unordered_food = food_parser.get_faculty_food()
        except TypeError:
            unordered_food = {'교직원식당': '오늘은 쉽니다.'}
        except Exception as inst:
            unordered_food = {'교직원식당': [
                inst,
                '파싱이 제대로 되지 않았습니다.',
                '일요일에는 메뉴가 없어서 동작하지 않을 수 있습니다.'
            ]}
        self.foods = OrderedDict(sorted(unordered_food.items()))

    def get_dict(self):
        return self.foods

    def get_string(self):
        dic = self.get_dict()
        self.prettify(dic)
        ret_string = self.prettified_str

        return ret_string

