import datetime
from .myLogger import viewLog
from .parser import food_api


class Menu:
    vacation_time_table = {
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
    time_table = {
        # 하드코딩 하는수밖에 없는거같음
        '학식': {
            '평일': {
                '조식': {
                    'start time': datetime.time(),
                    'end time': datetime.time(),
                },
                '중식': {
                    'start time': datetime.time(10, 20),
                    'end time': datetime.time(14, 00),
                },
                '석식': {
                    'start time': datetime.time(16, 30),
                    'end time': datetime.time(19, 00),
                },
            },
            '주말': {
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
            }
        },
        '교식': {
            '평일': {
                '조식': {
                    'start time': datetime.time(8, 00),
                    'end time': datetime.time(9, 00),
                },
                '중식': {
                    'start time': datetime.time(11, 20),
                    'end time': datetime.time(14, 00),
                },
                '석식': {
                    'start time': datetime.time(17, 00),
                    'end time': datetime.time(18, 30),
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

    look_up_order = '조식 조식1 조식2 중식 중식1 중식2 중식3 석식 석식1 석식2 특식'.split()

    @staticmethod
    def fetch_save_menu(date=None):
        def set_rate(f_dicts):
            for f_dict in f_dicts:
                for sec in f_dict:
                    f_dict[sec].update({
                        '평점': 0,
                        '참여자': [],
                    })

        try:
            from .managers import DBAdmin
            if DBAdmin.get_hakusiku_data(date):
                viewLog("fail", '오늘의 데이터는 이미 저장되어 있습니다.')
                return
            food_api.refresh(date)
            food_court = food_api.get_food_court()
            faculty_food = food_api.get_faculty_food()
            pupil_food = food_api.get_pupil_food()
            dorm_foods = food_api.get_dormitory_food(date)
            the_kitchen_food = food_api.get_the_kitchen()
            snack_corner_food = food_api.get_snack_corner()
            date = date or datetime.date.today()
            day_of_week = date.weekday()
            dorm_food = dorm_foods.get('월화수목금토일'[day_of_week])
            date = date.__str__()

            ratable_list = [faculty_food, pupil_food, dorm_food]
            set_rate(ratable_list)
            food_dict = {
                '푸드코트': food_court,
                '학식': pupil_food,
                '교식': faculty_food,
                '기식': dorm_food,
                '더 키친': the_kitchen_food,
                '스넥코너': snack_corner_food,
                '날짜': date,
            }
            viewLog('scheduler', food_dict)
            DBAdmin.set_hakusiku_data(food_dict, date)

        except Exception as e:
            viewLog("fail", e)

    def prepare_food(self, date=None):
        """
        draft of set_food func using hakusiku db
        :return: None
        """
        from .managers import DBAdmin
        data = DBAdmin.get_hakusiku_data(date)
        if data:
            self.foods = data[self.kor_name]
            viewLog("query", self.foods)

        else:
            try:
                self.fetch_save_menu(date)
                data = DBAdmin.get_hakusiku_data(date)
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
    def format_to_string(menu, place, date=None):
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

        today = date or datetime.date.today()
        day_of_week = "월화수목금토일"[today.weekday()]
        ret_string = '{}({}) {}\n'.format(today, day_of_week, place)
        if place in ['학식', '교식', '기식']:
            for time in Menu.look_up_order:
                if time in menu:
                    len_participant = len(menu[time]['참여자'])
                    star = rate2star(menu[time]['평점'])
                    ret_string += '\n{} {}({}명 평가)\n'.format(time, star, len_participant)
                    for dish in menu[time]['메뉴']:
                        ret_string += '*{}\n'.format(dish)
                    if place in ['학식', '교식']:
                        ret_string += '*{}\n'.format(menu[time]['가격'])
            return ret_string

        elif place == '푸드코트':
            ret_string += '\n'
            for dish in menu['메뉴']:
                ret_string += '*{}\n'.format(dish)
            return ret_string
        elif place == '더 키친':
            for dish in menu['메뉴']:
                if dish[-2:] in ['할인']:
                    ret_string += '\n{}\n'.format(dish)
                elif dish[0] in ['-', '*'] or dish == '카르보나라파스타 - 6.0':
                    ret_string += '\n{}\n'.format(dish)
                else:
                    ret_string += '*{}\n'.format(dish)
            return ret_string
        elif place == '스넥코너':
            for dish in menu['메뉴']:
                if dish[-1] in ['류'] or dish == '샌드위치':
                    ret_string += '\n{}\n'.format(dish)
                else:
                    ret_string += '*{}\n'.format(dish)
            return ret_string
        else:
            raise Exception('unexpected place: {}'.format(place))

    def get_string(self, date=None):
        dic = self.foods
        place = self.kor_name

        try:
            return Menu.format_to_string(dic, place, date)
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
the_kitchen_menu = Menu(kor_name='더 키친')
snack_corner_menu = Menu(kor_name='스넥코너')
