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
                self.prettified_str += '├──' * (indent + 1) + str(key)
                if isinstance(value, dict) or isinstance(value, list):
                    self.prettify(value, indent + 1)
                else:
                    self.prettified_str += '│  ├' + '─' * (indent + 1) + str(value)
        elif isinstance(d, list):
            for item in d:
                if isinstance(item, dict) or isinstance(item, list):
                    self.prettify(item, indent + 1)
                else:
                    if item == d[-1]:
                        self.prettified_str += '│  └' + '─' * (indent) + str(item)
                    else:
                        self.prettified_str += '│  ├' + '─' * (indent) + str(item)
        else:
            return Exception


class PupilMenu(Menu):
    def __init__(self):
        super().__init__()

    def set_pupil_foods(self):
        food_parser = FoodParser()
        food_parser.refresh()
        unordered_food = food_parser.get_pupil_food()
        self.foods = OrderedDict(sorted(unordered_food.items()))

    def get_dict(self):
        ret_dict = {}
        hangul = re.compile('[^가-힣 ]+')
        for section in self.foods:
            menu = self.foods[section][0]
            english_removed = hangul.sub('', menu)
            ret_dict.update({section: english_removed.split()})
        return ret_dict

    def get_string(self):
        dic = self.get_dict()
        self.prettify(dic)
        ret_string = self.prettified_str
        # dic = self.get_dict()
        # for section in dic:
        #     food_item = dic[section]
        #     ret_string += section + ':' + ', '.join(food_item)
        return ret_string


class FacultyMenu(Menu):
    def __init__(self):
        super().__init__()

    def set_faculty_foods(self):
        food_parser = FoodParser()
        food_parser.refresh()
        unordered_food = food_parser.get_faculty_food()
        self.foods = OrderedDict(sorted(unordered_food.items()))

    def get_dict(self):
        ret_dict = {}
        hangul = re.compile('[^가-힣 ]+')
        for section in self.foods:
            menu = self.foods[section][0]
            english_removed = hangul.sub('', menu)
            ret_dict.update({section: english_removed.split()})

        return ret_dict

    def get_string(self):
        ret_string = ''
        dic = self.get_dict()
        for section in dic:
            food_item = dic[section]
            ret_string += section + ':' + ', '.join(food_item)
        return ret_string
        # hangul = re.compile('[^가-힣 ]+')
        # for section in self.foods:
        #     menu = self.foods[section][0]
        #     english_removed = hangul.sub('', menu)
        #     ret_string += section + ':' + english_removed.rstrip() + '\n'
        return ret_string

