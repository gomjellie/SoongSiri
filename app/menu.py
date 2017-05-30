from .parser import FoodParser
import re


class Menu:
    def __init__(self):
        self.foods = None

    def get_foods(self):
        return self.foods

    def get_string(self):
        # 메뉴마다 깔끔하게 딕셔너리를 string으로 바꾼다
        pass


class PupilMenu(Menu):
    def __init__(self):
        super().__init__()

    def set_pupil_foods(self):
        food_parser = FoodParser()
        food_parser.refresh()
        self.foods = food_parser.get_pupil_food()

    def get_string(self):
        ret_string = ''
        hangul = re.compile('[^가-힣 ]+')
        for section in self.foods:
            menu = self.foods[section][0]
            english_removed = hangul.sub('', menu)
            ret_string += section + ':' + english_removed.rstrip() + '\n'
        return ret_string


class FacultyMenu(Menu):
    def __init__(self):
        super().__init__()

    def set_faculty_foods(self):
        food_parser = FoodParser()
        food_parser.refresh()
        self.foods = food_parser.get_faculty_food()

    def get_string(self):
        ret_string = ''
        hangul = re.compile('[^가-힣 ]+')
        for section in self.foods:
            menu = self.foods[section][0]
            english_removed = hangul.sub('', menu)
            ret_string += section + ':' + english_removed.rstrip() + '\n'
        return ret_string

