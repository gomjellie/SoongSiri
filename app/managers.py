from .message import *
from app import session
from functools import wraps
import datetime


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
    }

    PROCESS = {
        '식단 별점주기': [
            {
                '식단 별점주기': SelectFoodPlaceMessage,
            },
            {
                '학식': RatingPupilMessage,
                '교식': RatingFacultyMessage,
                '기식': RatingDormFoodMessage,
            },
            {
                '조식': RateFoodMessage,
                '중식': RateFoodMessage,
                '석식': RateFoodMessage,
                # '중.석식': RateFoodMessage,
            },
            {
                '맛있음': RateFoodEndMessage,
                '보통': RateFoodEndMessage,
                '맛없음': RateFoodEndMessage,
            },
        ],
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
        '도서관': [
            {
                '도서관': LibMessage,
            },
            {
                # 일단 예외로 둔다
                '*': OnGoingMessage,
            }
        ],
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

        if process == '식단 별점주기':
            if content in self.PROCESS[process][1]:
                # 학식, 교식 중식
                new_msg = self.PROCESS[process][1][content]
                return new_msg()
            elif content[:2] in self.PROCESS[process][2]:
                # 조식 중식 석식
                hist = UserSessionAdmin.get_history(user_key)
                place, menu = hist[-2:]
                menu = menu[:2]  # 조식2->조식
                from .menu import Menu
                is_available, start_time, end_time = Menu.is_available_now(place, menu)
                if is_available:
                    new_msg = self.PROCESS[process][2][menu]
                    return new_msg()
                else:
                    UserSessionAdmin.delete(user_key)
                    return FoodNonVotableMessage(start_time, end_time)
            elif content in self.PROCESS[process][3]:
                # 맛있음 보통 맛없음
                hist = UserSessionAdmin.get_history(user_key)
                place, menu, rate = hist[-3:]
                prev_rate, new_rate = DBAdmin.update_rate(user_key, place, menu, rate)
                UserSessionAdmin.delete(user_key)
                new_msg = self.PROCESS[process][3][content]
                return new_msg(prev_rate, new_rate)
            else:
                UserSessionAdmin.delete(user_key)
                return FailMessage('식단 별점주기 process에서 문제가 발생하였습니다 해당 세션을 초기화합니다.')
        elif process == '도서관':
            if '열람실' in content:
                room = content[0]  # '1 열람실 (이용률: 9.11%)'[0]하면 1만 빠져나온다
                msg = LibStatMessage(room=room)
                UserSessionAdmin.delete(user_key)
            else:
                UserSessionAdmin.delete(user_key)
                msg = FailMessage('도서관 process에서 문제가 발생하였습니다 해당 세션을 초기화합니다.')
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
                new_msg = FailMessage('내일의 식단 process에서 문제가 발생하였습니다 해당 세션을 초기화합니다.')
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
        else:
            return FailMessage("stat not in list('home', 'message', 'fail')")


class SessionManager(metaclass=Singleton):
    def check_user_key(self, user_key):
        if user_key in session:
            return True
        else:
            return False

    def verify_session(func):
        @wraps(func)
        def session_wrapper(*args, **kwargs):
            user_key = args[1]
            if user_key in session:
                return func(*args, **kwargs)
            else:
                return False

        return session_wrapper

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
        session[user_key]['history'].append(content)

    @verify_session
    def get_history(self, user_key):
        return session[user_key]['history'][:]

    @verify_session
    def init_process(self, user_key, process):
        session[user_key]['process'] = process

    @verify_session
    def expire_process(self, user_key):
        session[user_key]['process'] = None

    @verify_session
    def get_process(self, user_key):
        return session[user_key].get('process')


class DBManager:
    def __init__(self):
        import pymongo
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

        review = self.get_review()

        if count_user_key(review['리뷰']) < 3:
            review['리뷰'].append({'user_key': user_key, 'content': new_review})
            self.review.find_one_and_replace({'날짜': datetime.date.today().__str__()}, review)
        else:
            raise Exception('3회 이상 작성하셨습니다.')

    def update_rate(self, user_key, place, menu, rate):
        today = datetime.date.today().__str__()

        data = self.hakusiku.find_one({'날짜': today})

        participant = data[place][menu]['참여자']
        prev_rate = data[place][menu]['평점']
        score = {
            "맛있음": 10.0,
            "보통": 5.0,
            "맛없음": 1,
        }
        rate = score[rate]

        if user_key in participant:
            from .my_exception import FoodRateDuplicate

            raise FoodRateDuplicate()
        else:
            _prev_rate = prev_rate * len(participant)
            participant.append(user_key)
            new_rate = (_prev_rate + rate) / len(participant)
            data[place][menu]['평점'] = new_rate

            self.hakusiku.find_one_and_replace({"날짜": today}, data)
            return prev_rate, new_rate


APIAdmin = APIManager()
UserSessionAdmin = SessionManager()
DBAdmin = DBManager()
