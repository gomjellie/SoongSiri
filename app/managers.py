from .message import *
from app.keyboard import Keyboard

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
                    bus_message.front()
                elif content == '베라 앞(20165)':
                    bus_message.bera()
                elif content == '중문(20169)':
                    bus_message.middle()
                return bus_message
            elif content == '도서관' or '열람실' in content:
                lib_message = LibMessage()
                if '열람실' in content:
                    room_no = content[0]
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


class MessageManager(metaclass=Singleton):
    def get_home_message(self):
        return HomeMessage()

    def get_food_message(self):
        return FoodMessage()

    def get_fail_message(self):
        return FailMessage()

    def get_on_going_message(self):
        return OnGoingMessage()


class KeyboardManager(metaclass=Singleton):
    pass

APIAdmin = APIManager()
MessageAdmin = MessageManager()
