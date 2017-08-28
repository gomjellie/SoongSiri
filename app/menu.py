import datetime
from .myLogger import viewLog
from .parser import food_api


class Menu:
    time_table = {
        # 하드코딩 하는수밖에 없는거같음
        '학식': {
            '평일': {
                '조식': {
                    'start time': datetime.time(),
                    'end time': datetime.time(),
                },
                '중식': {
                    'start time': datetime.time(10, 30),
                    'end time': datetime.time(14, 00),
                },
                '석식': {
                    'start time': datetime.time(),
                    'end time': datetime.time(),
                },
            },
            '주말': {
                '조식': {
                    'start time': datetime.time(),
                    'end time': datetime.time(),
                },
                '중식': {
                    'start time': datetime.time(),
                    'end time': datetime.time(),
                },
                '석식': {
                    'start time': datetime.time(),
                    'end time': datetime.time(),
                },
            }
        },
        '교식': {
            '평일': {
                '조식': {
                    'start time': datetime.time(),
                    'end time': datetime.time(),
                },
                '중식': {
                    'start time': datetime.time(11, 30),
                    'end time': datetime.time(14, 00),
                },
                '석식': {
                    'start time': datetime.time(17, 00),
                    'end time': datetime.time(18, 10),
                },
            },
            '주말': {
                '조식': {
                    'start time': datetime.time(),
                    'end time': datetime.time(),
                },
                '중식': {
                    'start time': datetime.time(11, 30),
                    'end time': datetime.time(14, 00),
                },
                '석식': {
                    'start time': datetime.time(),
                    'end time': datetime.time(),
                },
            }
        },
        '기식': {
            '평일': {
                '조식': {
                    'start time': datetime.time(8, 0),
                    'end time': datetime.time(9, 30),
                },
                '중식': {
                    'start time': datetime.time(11, 00),
                    'end time': datetime.time(14, 00),
                },
                '석식': {
                    'start time': datetime.time(17, 00),
                    'end time': datetime.time(18, 30),
                },
            },
            '주말': {
                '조식': {
                    'start time': datetime.time(8, 0),
                    'end time': datetime.time(9, 30),
                },
                '중식': {
                    'start time': datetime.time(11, 00),
                    'end time': datetime.time(14, 00),
                },
                '석식': {
                    'start time': datetime.time(17, 00),
                    'end time': datetime.time(18, 30),
                },
            }
        },
    }

    def __init__(self, kor_name):
        """
        :param open_time: '2017-07-03 이런 형태'
        :param kor_name: '학식, 교식, 푸드코트 중에 하나이다.'
        """
        self.foods = None
        self.kor_name = kor_name

    look_up_order = '조식 조식1 조식2 중식 중식1 중식2 석식 석식1 석식2'.split()

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
            dorm_food = dorm_foods.get('월화수목금토일'[day_of_week])
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

        except Exception as e:
            viewLog("fail", e)

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
        for time in Menu.look_up_order:
            if time in self.foods:
                ret.append(time)
        return ret

    @staticmethod
    def format_to_string(menu, place):
        def rate2star(rate):
            # half = '✮'
            # full = '★'
            # empty = '✩'
            stars = [
                '✩✩✩✩✩',
                '✮✩✩✩✩',
                '★✩✩✩✩',
                '★✩✩✩✩',
                '★✮✩✩✩',
                '★★✮✩✩',
                '★★★✩✩',
                '★★★✮✩',
                '★★★★✩',
                '★★★★✮',
                '★★★★★',
            ]
            return stars[round(rate)]

        today = datetime.date.today()
        ret_string = '{} {}\n'.format(today, place)
        if place in ['학식', '교식', '기식']:
            for time in Menu.look_up_order:
                if time in menu:
                    star = rate2star(menu[time]['평점'])
                    ret_string += '\n{} {}\n'.format(time, star)
                    for dish in menu[time]['메뉴']:
                        ret_string += '*{}\n'.format(dish)
                    ret_string += '*{}\n'.format(menu[time]['가격'])
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
            raise FoodNotFound(e)

    @staticmethod
    def is_available_now(place, menu):
        time_table = Menu.time_table
        current_time = datetime.datetime.now().time()
        today = datetime.date.today()
        day_of_week = today.weekday()
        is_weekend = '주말' if day_of_week in [5, 6] else '평일'
        start_time = time_table[place][is_weekend][menu]['start time']
        end_time = time_table[place][is_weekend][menu]['end time']

        if start_time < current_time < end_time:
            return True, start_time, end_time
        else:
            return False, start_time, end_time


pupil_menu = Menu(kor_name='학식')
faculty_menu = Menu(kor_name='교식')
food_court_menu = Menu(kor_name='푸드코트')
dormitory_menu = Menu(kor_name='기식')
