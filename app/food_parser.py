from bs4 import BeautifulSoup
import requests


class FoodParser():
    def __init__(self):
        self.base_url = 'http://soongguri.com/menu/m_menujson.php'
        self.faculty_food = None
        self.pupil_food = None
        self.the_kitchen = None
        self.snack_corner = None
        self.food_court = None

    def refresh(self):
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
        :return:
        """
        ret_dict = {}
        for section in self.the_kitchen:
            ret_dict.update({section: []})
            soup = BeautifulSoup(self.the_kitchen[section], 'html.parser')
            ret_dict[section].append(soup.text)
        return ret_dict

    def get_snack_corner(self):
        """
            :return:
            TODO: 정규표현식 이용해서 메뉴 가격 깔끔하게 나누기
        """
        ret_dict = {}
        for section in self.snack_corner:
            ret_dict.update({section: []})
            soup = BeautifulSoup(self.snack_corner[section], 'html.parser')
            ret_dict[section].append(soup.text)
        return ret_dict

    def get_food_court(self):
        """
            :return:
            TODO: 정규표현식 이용해서 메뉴 가격 깔끔하게 나누기
        """
        ret_dict = {}
        for section in self.food_court:
            ret_dict.update({section: []})
            soup = BeautifulSoup(self.food_court[section], 'html.parser')
            ret_dict[section].append(soup.text)
        return ret_dict
