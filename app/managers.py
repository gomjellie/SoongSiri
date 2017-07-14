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
    def process(self, stat, req=None):
        if stat is 'home':
            home_message = MessageAdmin.get_home_message()
            return home_message
        else:
            content = req['content']
            user_key = req['user_key']

            if content == u'식단 보기':
                return MessageAdmin.get_food_message()
            elif content == u'식단 평가':
                session[user_key] = '식단 평가'
                return MessageAdmin.get_on_going_message()
            elif content in ['학식', '교식', '푸드코트']:
                if content == '학식':
                    return PupilFoodMessage()
                elif content == '교식':
                    return FacultyFoodMessage()
                elif content == '푸드코트':
                    return FoodCourtMessage()
                else:
                    raise Exception('unexpected button {}'.format(content))
            elif content in ['정문(20166)', '베라 앞(20165)','중문(20169)', '버스']:
                bus_message = BusMessage()
                if content == '정문(20166)':
                    bus_message = BusFrontMessage()
                elif content == '베라 앞(20165)':
                    bus_message = BusBeraMessage()
                elif content == '중문(20169)':
                    bus_message = BusMiddleMessage()
                return bus_message
            elif content == '도서관' or '열람실' in content:
                lib_message = LibMessage()
                if '열람실' in content:
                    room_no = content[0]    # '1 열람실 (이용률: 9.11%)'[0]하면 1만 빠져나온다
                    lib_message.select_room(room_no)
                return lib_message
            elif content == '지하철':
                return SubMessage()
            elif content == 'fail':
                on_going_message = MessageAdmin.get_on_going_message()
                on_going_message.update_message(req['log'])
                return on_going_message
            else:
                raise Exception("unexpected req['content']")


class SessionManager(metaclass=Singleton):
    def checkExist(self, user_key):
        if user_key in session:
            return True
        else:
            return False

    def check_session(self, func):
        @wraps
        def wrapper(user_key, *args, **kwargs):
            if self.checkExist(user_key):
                func()
        return wrapper

    def check_process(self, func):
        @wraps
        def wrapper(user_key, *args, **kwargs):
            if session[user_key]['process'][0]:
                func()
        return wrapper

    def init(self, user_key, content):
        session[user_key] = {
            'history': [content],
            'process': (None, None),
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
        session[user_key]['process'] = (process, 1)

    @check_session
    def next_process(self, user_key):
        process, step = session[user_key]['process']
        session[user_key]['process'] = (process, step+1)

    @check_session
    def expire_process(self, user_key):
        session[user_key]['process'] = (None, None)

    @check_process
    @check_session
    def get_process(self, user_key):
        return session[user_key]['process']


class MessageManager(metaclass=Singleton):
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
                '식단 평가': RatingFoodMessage,
            },
            {
                '학식': RatingPupilMessage,
                '교식': RatingFacultyMessage,
                '푸드코트': RatingFoodCourtMessage,
            },
            {
                '맛있음': OnGoingMessage,
                '보통': OnGoingMessage,
                '맛없음': OnGoingMessage,
            },
            {

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
        MessageManager.PROCESS 의 항목들을 처리한다.

        :return: Message Object
        """
        prs, step = UserSessionAdmin.get_process(user_key)
        if process == '식단 평가':
            if content in MessageManager.PROCESS[process][1]:
                new_msg = MessageManager.PROCESS[process][1][content]
                return new_msg()
            elif content in MessageManager.PROCESS[process][2]:
                hist = UserSessionAdmin.get_history(user_key)
                place = hist[-2]
                # update database HERE

                UserSessionAdmin.delete(user_key)

            if step+1 == len(MessageManager.PROCESS[process]):
                UserSessionAdmin.expire_process(user_key)

        elif process == '도서관':
            if '열람실' in content:
                room = content[0]  # '1 열람실 (이용률: 9.11%)'[0]하면 1만 빠져나온다
                msg = LibMessage(room=room)
            return msg

    def handle(self, user_key, content):
        has_session = UserSessionAdmin.checkExist(user_key)
        process, step = UserSessionAdmin.get_process(user_key)

        if not has_session:
            UserSessionAdmin.init(user_key, content)

        UserSessionAdmin.add_history(user_key, content)
        if process:
            new_msg = MessageManager.PROCESS[process][step][content]
            UserSessionAdmin.next_process(user_key)
            if step+1 == len(MessageManager.PROCESS[process]):
                UserSessionAdmin.expire_process(user_key)
            return new_msg()
        else:
            if content in MessageManager.PROCESS:
                UserSessionAdmin.init_process(user_key, content)
                new_msg = MessageManager.PROCESS[content][0][content]
                return new_msg()
            else:
                new_msg = MessageAdmin.FREE_PROCESS[content]
                return new_msg()


class DBManager:
    def get_data(self, date=None):
        if not date:
            today = datetime.datetime.today().__str__()
        data = hakusiku.find_one({'날짜': today})
        return data

    def add_rating(self, user_key, place, menu, rate):
        today = datetime.datetime.today().__str__()
        data = hakusiku.find_one({'날짜': today})


class KeyboardManager(metaclass=Singleton):
    pass

APIAdmin = APIManager()
MessageAdmin = MessageManager()
UserSessionAdmin = SessionManager()
