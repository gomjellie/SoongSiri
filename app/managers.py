from .message import *
from app import session
from app import hakusiku
import datetime
from functools import wraps


class Singleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class APIManager(metaclass=Singleton):
    FREE_PROCESS = {
        '식단 보기': FoodMessage,
        '학식': PupilFoodMessage,
        '교식': FacultyFoodMessage,
        '푸드코트': FoodCourtMessage,
        '버스': BusMessage,
        '정문(20166)': BusFrontMessage,
        '베라 앞(20165)': BusBeraMessage,
        '중문(20169)': BusMiddleMessage,
        '지하철': SubMessage,
    }

    PROCESS = {
        '식단 평가': [
            {
                '식단 평가': SelectFoodPlaceMessage,
            },
            {
                '학식': RatingPupilMessage,
                '교식': RatingFacultyMessage,
                '푸드코트': RatingFoodCourtMessage,
            },
            {
                '조식1': RateFoodMessage,
                '조식2': RateFoodMessage,
                '중식1': RateFoodMessage,
                '중식2': RateFoodMessage,
                '석식1': RateFoodMessage,
                '석식2': RateFoodMessage,
            },
            {
                '맛있음': OnGoingMessage,
                '보통': OnGoingMessage,
                '맛없음': OnGoingMessage,
            },
        ],

        '도서관': [
            {
                '도서관': LibMessage,
            },
            {
                # 일단 예외로 둔다
                '*': OnGoingMessage,
            }
        ]
    }

    def handle_process(self, process, user_key, content):
        """
        self.PROCESS 의 항목들을 처리한다.

        :return: Message Object
        """

        if process == '식단 평가':
            if content in self.PROCESS[process][1]:
                new_msg = self.PROCESS[process][1][content]
                return new_msg()
            elif content in self.PROCESS[process][2]:
                new_msg = self.PROCESS[process][2][content]
                return new_msg()
            elif content in self.PROCESS[process][3]:
                hist = UserSessionAdmin.get_history(user_key)
                place = hist[-3]
                menu = hist[-2]
                rate = hist[-1]
                # update database HERE
                DatabaseAdmin.update_rate(user_key, place, menu, rate)

                UserSessionAdmin.delete(user_key)
                new_msg = self.PROCESS[process][2][content]

                UserSessionAdmin.expire_process(user_key)
                return new_msg()

        elif process == '도서관':
            if '열람실' in content:
                room = content[0]  # '1 열람실 (이용률: 9.11%)'[0]하면 1만 빠져나온다
                msg = LibMessage(room=room)
                UserSessionAdmin.expire_process(user_key)
            else:
                msg = FailMessage()
            return msg

    def handle_free_process(self, user_key, content):
        """
        FREE_PROCESS 항목들을 처리한다.

        :param user_key:
        :param content:
        :return: Message Object
        """
        if content in self.PROCESS:
            UserSessionAdmin.init_process(user_key, content)
            new_msg = self.PROCESS[content][0][content]
            return new_msg()
        else:
            new_msg = self.FREE_PROCESS[content]
            return new_msg()

    def get_msg(self, user_key, content):
        has_session = UserSessionAdmin.check_user_key(user_key)
        process = UserSessionAdmin.get_process(user_key)

        if not has_session:
            UserSessionAdmin.init(user_key, content)

        UserSessionAdmin.add_history(user_key, content)
        if process:
            return self.handle_process(process, user_key, content)

        else:
            return self.handle_free_process(user_key, content)

    def process(self, stat, req=None):
        if stat is 'home':
            home_message = HomeMessage()
            return home_message
        elif stat is 'message':
            content = req['content']
            user_key = req['user_key']

            return self.get_msg(user_key, content)

        elif stat is 'fail':
            log = req['log']
            fail_message = FailMessage()
            fail_message.update_message(log)
            return fail_message
        else:
            return FailMessage()


class SessionManager(metaclass=Singleton):
    def check_user_key(self, user_key):
        if user_key in session:
            return True
        else:
            return False

    def check_session(self, func):
        @wraps
        def session_wrapper(user_key, *args, **kwargs):
            if self.check_user_key(user_key):
                func()
            else:
                return False
        return session_wrapper

    def check_process(self, func):
        @wraps
        def process_wrapper(user_key, *args, **kwargs):
            if 'process' in session[user_key]['process']:
                func()
            else:
                return False
        return process_wrapper

    def init(self, user_key, content):
        session[user_key] = {
            'history': [content],
            'process': None,
            # process[0]: process name, process[1]: process step
        }

    @check_session
    def delete(self, user_key):
        del session[user_key]

    @check_session
    def add_history(self, user_key, content):
        session[user_key].append(content)

    @check_session
    def get_history(self, user_key):
        return session[user_key]['history'][:]

    @check_session
    def init_process(self, user_key, process):
        session[user_key]['process'] = process

    @check_session
    def next_process(self, user_key):
        process, step = session[user_key]['process']
        session[user_key]['process'] = (process, step+1)

    @check_session
    def expire_process(self, user_key):
        session[user_key]['process'] = None

    @check_process
    @check_session
    def get_process(self, user_key):
        return session[user_key]['process']


class DBManager:
    def get_data(self, date=None):
        if not date:
            today = datetime.datetime.today().__str__()
        data = hakusiku.find_one({'날짜': today})
        return data

    def update_rate(self, user_key, place, menu, rate):
        today = datetime.datetime.today().__str__()
        data = hakusiku.find_one({'날짜': today})


class KeyboardManager(metaclass=Singleton):
    pass

APIAdmin = APIManager()
UserSessionAdmin = SessionManager()
DatabaseAdmin = DBManager()

