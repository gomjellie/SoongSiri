import datetime
from app import myLogger


class Menu:
    def __init__(self, kor_name):
        """
        :param open_time: '2017-07-03 이런 형태'
        :param kor_name: '학식, 교식, 푸드코트 중에 하나이다.'
        """
        self.foods = None
        self.kor_name = kor_name

    def fetch_food(self):
        """
        draft of set_food func using hakusiku db
        :return: None
        """
        from .managers import DBManager
        data = DBManager.get_data()
        if data:
            self.foods = data[self.kor_name]
            myLogger.viewLog("query", self.foods)

        else:
            try:
                from .scheduler import menu_scheduler

                menu_scheduler.fetch_save_menu()
                data = DBManager.get_data()
                print(data)
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

