import datetime
from .myLogger import viewLog
from .parser import food_api


class Menu:
    def __init__(self, kor_name):
        """
        :param open_time: '2017-07-03 이런 형태'
        :param kor_name: '학식, 교식, 푸드코트 중에 하나이다.'
        """
        self.foods = None
        self.kor_name = kor_name

    @staticmethod
    def fetch_save_menu():
        def set_rate(f_dicts):
            for f_dict in f_dicts:
                for sec in f_dict:
                    f_dict[sec].update({
                        '평점': 0,
                        '참여자': [],
                    })
        try:
            from .managers import DBAdmin
            if DBAdmin.get_data():
                viewLog("fail", '오늘의 데이터는 이미 저장되어 있습니다.')
                return
            food_api.refresh()
            food_court = food_api.get_food_court()
            faculty_food = food_api.get_faculty_food()
            pupil_food = food_api.get_pupil_food()
            dorm_foods = food_api.get_dormitory_food()
            day_of_week = datetime.date.today().weekday()
            dorm_food = dorm_foods.get(' 월화수목금토일'[day_of_week])
            date = datetime.date.today().__str__()

            ratable_list = [faculty_food, pupil_food, dorm_food]
            set_rate(ratable_list)
            food_dict = {
                '푸드코트': food_court,
                '학식': pupil_food,
                '교식': faculty_food,
                '기식': dorm_food,
                '날짜': date,
            }
            viewLog('scheduler', food_dict)
            DBAdmin.set_data(food_dict)

        except Exception as inst:
            viewLog("fail", inst.__str__())

    def prepare_food(self):
        """
        draft of set_food func using hakusiku db
        :return: None
        """
        from .managers import DBAdmin
        data = DBAdmin.get_data()
        if data:
            self.foods = data[self.kor_name]
            viewLog("query", self.foods)

        else:
            try:
                self.fetch_save_menu()
                data = DBAdmin.get_data()
                self.foods = data[self.kor_name]
            except Exception as e:
                from .my_exception import FoodNotFound
                raise FoodNotFound(e)

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
    def format_to_string(menu, place):
        today = datetime.date.today().__str__()
        ret_string = '{} {}\n'.format(today, place)
        if place in ['학식', '교식', '기식']:
            for time in menu:
                ret_string += '\n{} (평점 {:0.2f}/10.0)\n'.format(time, menu[time]['평점'])
                for dish in menu[time]['메뉴']:
                    ret_string += '*{}\n'.format(dish)
            return ret_string
        elif place == '푸드코트':
            for dish in menu['메뉴']:
                ret_string += '*{}\n'.format(dish)
            return ret_string
        else:
            raise Exception('unexpected place: {}'.format(place))

    def get_string(self):
        dic = self.foods
        place = self.kor_name

        try:
            return Menu.format_to_string(dic, place)
        except Exception as e:
            from .my_exception import FoodNotFound
            raise FoodNotFound(e.__str__())

pupil_menu = Menu(kor_name='학식')
faculty_menu = Menu(kor_name='교식')
food_court_menu = Menu(kor_name='푸드코트')
dormitory_menu = Menu(kor_name='기식')

