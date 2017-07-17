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


def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('init func {} with args: {} kwargs: {}'.format(func.__name__, args, kwargs))
        return func(*args, **kwargs)
    return wrapper


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

    @logger
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

    @logger
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

    @logger
    def get_msg(self, user_key, content):
        has_session = UserSessionAdmin.check_user_key(user_key)
        process = UserSessionAdmin.get_process(user_key)
        print(process)

        if not has_session:
            UserSessionAdmin.init(user_key, content)

        UserSessionAdmin.add_history(user_key, content)
        if process:
            return self.handle_process(process, user_key, content)

        else:
            return self.handle_free_process(user_key, content)

    @logger
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

    @logger
    def verify_session(func):
        @wraps(func)
        def session_wrapper(*args, **kwargs):
            user_key = args[1]
            if user_key in session:
                return func(*args, **kwargs)
            else:
                print('user_key: {} is not in session'.format(user_key))
                return False
        return session_wrapper

    @logger
    def init(self, user_key, content=None, process=None):
        session[user_key] = {
            'history': [content],
            'process': process,
            # process[0]: process name, process[1]: process step
        }

    @verify_session
    def delete(self, user_key):
        del session[user_key]

    @verify_session
    def add_history(self, user_key, content):
        session[user_key].append(content)

    @verify_session
    def get_history(self, user_key):
        return session[user_key]['history'][:]

    @verify_session
    def init_process(self, user_key, process):
        session[user_key]['process'] = process

    @verify_session
    def next_process(self, user_key):
        process, step = session[user_key]['process']
        session[user_key]['process'] = (process, step+1)

    @verify_session
    def expire_process(self, user_key):
        session[user_key]['process'] = None

    @verify_session
    def get_process(self, user_key):
        return session[user_key].get('process')


class DBManager:
    def get_data(self, date=None):
        if date is None:
            today = datetime.datetime.today().__str__()
        else:
            today = date
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

