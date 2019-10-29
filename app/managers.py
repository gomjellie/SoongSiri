from .message import *
from functools import wraps
import datetime
import pymongo
import re
from app import session


class Singleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class APIManager(metaclass=Singleton):
    STATELESS_PROCESS = {
        '오늘의 식단': FoodMessage,
        '운영시간': TimeTableMessage,
        '학식': PupilFoodMessage,
        '교식': FacultyFoodMessage,
        '기식': DormFoodMessage,
        '푸드코트': FoodCourtMessage,
        '스낵코너': SnackCornerMessage,
        '더 키친': TheKitchenMessage,
        '버스': BusMessage,
        '정문(20166)': BusFrontMessage,
        '베라 앞(20165)': BusBeraMessage,
        '중문(20169)': BusMiddleMessage,
        '지하철': SubMessage,
        '도서관': LibMessage,
    }

    PROCESS = {
        '내일의 식단': [
            {
                '내일의 식단': TomorrowFoodMessage,
            },
            {
                '학식': TomorrowPupilFoodMessage,
                '교식': TomorrowFacultyFoodMessage,
                '기식': TomorrowDormFoodMessage,
                '푸드코트': TomorrowFoodCourtMessage,
                '스낵코너': TomorrowSnackCornerMessage,
                '더 키친': TomorrowTheKitchenMessage,
            },
        ],
        # '도서관': [
        #     {
        #         '도서관': LibMessage,
        #     },
        #     {
        #         # 일단 예외로 둔다
        #         '*': OnGoingMessage,
        #     }
        # ],
        '식단 리뷰': [
            {
                '식단 리뷰': ReviewInitMessage,
            },
            {
                '리뷰 보기': ReviewBrowseMessage,
                '리뷰 남기기': ReviewPostMessage,
                '리뷰 삭제하기': OnGoingMessage,
            },
            {
                # 리뷰 남기기 하면 3단계까지 옴 키보드로 입력받은 문자열이 오기때문에 가능성이 다양함
                '*': OnGoingMessage,
            }
        ],
    }

    def handle_process(self, process, user_key, content):
        """
        연속되는 문답이 필요한 항목들을 처리한다.

        :return: Message Object
        """

        if process == '도서관':
            if '열람실' in content:
                room = content[0]  # '1 열람실 (이용률: 9.11%)'[0]하면 1만 빠져나온다
                msg = LibStatMessage(room=room)
                UserSessionAdmin.delete(user_key)
            else:
                UserSessionAdmin.delete(user_key)
                return FailMessage('도서관 process에서 문제가 발생하였습니다 해당 세션을 초기화합니다.')
            return msg
        elif process == '식단 리뷰':
            if content in self.PROCESS[process][1]:
                new_msg = self.PROCESS[process][1][content]
                if content in ['리뷰 보기', '리뷰 삭제']:
                    UserSessionAdmin.delete(user_key)
                return new_msg()
            else:
                UserSessionAdmin.delete(user_key)
                return ReviewPostSuccess(user_key, content)
        elif process == '내일의 식단':
            if content in self.PROCESS[process][1]:
                new_msg = self.PROCESS[process][1][content]
                UserSessionAdmin.delete(user_key)
            else:
                UserSessionAdmin.delete(user_key)
                return FailMessage('내일의 식단 process에서 문제가 발생하였습니다 해당 세션을 초기화합니다.')
            return new_msg()
        return FailMessage('Unhandled process {}'.format(process))

    def handle_stateless_process(self, user_key, content):
        """
        연속적이지 않은 항목들을 처리한다.

        :param user_key:
        :param content:
        :return: Message Object
        """

        if content in self.PROCESS:
            UserSessionAdmin.init_process(user_key, content)
            new_msg = self.PROCESS[content][0][content]
            return new_msg()
        else:
            new_msg = self.STATELESS_PROCESS[content]
            return new_msg()

    def get_msg(self, user_key, content):
        has_session = UserSessionAdmin.check_user_key(user_key)
        process = UserSessionAdmin.get_process(user_key)

        if not has_session:
            UserSessionAdmin.init(user_key, content)

        if content == '취소':
            UserSessionAdmin.delete(user_key)
            return CancelMessage()

        UserSessionAdmin.add_history(user_key, content)
        if process:
            return self.handle_process(process, user_key, content)

        else:
            return self.handle_stateless_process(user_key, content)

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
            user_key = req['user_key']
            fail_message = FailMessage('파악할수 없는 에러가 발생하여 해당 세션을 초기화 합니다\n{}'.format(log))
            UserSessionAdmin.delete(user_key)
            return fail_message
        elif stat is 'etc':
            return SuccessMessage()
        elif stat is "scheduler":
            return CronUpdateMessage()
        elif stat is "refresh_tomorrow":
            return CronUpdateTomorrowMessage()
        else:
            return FailMessage("stat not in list('home', 'message', 'fail')")


class SessionManager(metaclass=Singleton):
    @staticmethod
    def check_user_key(user_key):
        if session.find_one({'user_key': user_key}):
            return True
        else:
            return False

    def verify_session(func):
        @wraps(func)
        def session_wrapper(*args, **kwargs):
            user_key = args[1]
            if session.find_one({'user_key': user_key}):
                return func(*args, **kwargs)
            else:
                return False

        return session_wrapper

    def init(self, user_key, content=None, process=None):
        session.insert_one({
            'user_key': user_key,
            'history': [content],
            'process': process,
        })

    @verify_session
    def delete(self, user_key):
        session.remove({'user_key': user_key})

    @verify_session
    def add_history(self, user_key, content):
        user = session.find_one({'user_key': user_key})
        history = user['history']
        history.append(content)
        user.update({'history': history})
        session.save(user)

    @verify_session
    def get_history(self, user_key):
        user = session.find_one({'user_key': user_key})
        history = user['history']
        return history[:]

    @verify_session
    def init_process(self, user_key, process):
        user = session.find_one({'user_key': user_key})
        user.update({'process': process})
        session.save(user)

    @verify_session
    def expire_process(self, user_key):
        user = session.find_one({'user_key': user_key})
        user.update({'process': None})
        session.save(user)

    @verify_session
    def get_process(self, user_key):
        user = session.find_one({'user_key': user_key})
        return user['process']


class DBManager:
    def __init__(self):
        _conn = pymongo.MongoClient()
        _food_db = _conn.food_db
        self.hakusiku = _food_db.hakusiku
        self.review = _food_db.review
        self.ban_list = _food_db.ban_list
        if self._get_black_list() is None:
            self.ban_list.insert_one({'black_list': []})

    def get_hakusiku_data(self, date=None):
        date = date or datetime.date.today()
        date_str = date.__str__()
        data = self.hakusiku.find_one({'날짜': date_str})
        return data

    def set_hakusiku_data(self, data, date=None):
        date = date or datetime.date.today()
        date_str = date.__str__()
        if self.get_hakusiku_data(date=date_str) is None:
            self.hakusiku.insert_one(data)
        else:
            self.hakusiku.replace_one({"날짜": date_str}, data)

    def is_banned_user(self, user_key):
        return True if user_key in self._get_black_list() else False

    def _get_black_list(self):
        return self.ban_list.find_one({}, {'_id': 0, 'black_list': 1})

    def ban_user(self, user_key):
        black_list = self._get_black_list()
        black_list.append(user_key)

    def get_review(self):
        date = datetime.date.today().__str__()
        data = self.review.find_one({'날짜': date}) or self.init_review()
        return data

    def init_review(self):
        date = datetime.date.today().__str__()
        self.review.insert_one({
            '날짜': date,
            '리뷰': [],
        })
        return self.get_review()

    def append_review(self, user_key: str, new_review: str):
        def count_user_key(lst):
            # TODO: mongodb 기능에 count 하는게 있을듯 그걸로 대체
            s = 0
            for i in lst:
                if i.get('user_key') == user_key:
                    s += 1
            return s

        def remove_special_char(src):
            return re.sub("[!@#$%^&*()]", "", src)

        review = self.get_review()

        if count_user_key(review['리뷰']) < 5:
            review['리뷰'].append({'user_key': user_key, 'content': remove_special_char(new_review)})
            self.review.find_one_and_replace({'날짜': datetime.date.today().__str__()}, review)
        else:
            raise Exception('5회 이상 작성하셨습니다.')


APIAdmin = APIManager()
UserSessionAdmin = SessionManager()
DBAdmin = DBManager()
