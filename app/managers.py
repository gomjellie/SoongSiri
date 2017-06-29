from .message import *


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
            if content == u'식단 보기':
                return MessageAdmin.get_food_message()
            elif content == u'식단 평가':
                return MessageAdmin.get_fail_message()
            elif content in ['학식', '교식']:
                if content == '학식':
                    return PupilFoodMessage()
                elif content == '교식':
                    return FacultyFoodMessage()
            elif content in ['버스', '정문', '정문 건너편(베라 앞)', '중문']:
                bus_message = BusMessage()
                if content == '정문':
                    bus_message.front()
                elif content == '정문 건너편(베라 앞)':
                    bus_message.bera()
                elif content == '중문':
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
            elif content == 'on_going':
                on_going_message = MessageAdmin.get_on_going_message()
                on_going_message.update_message(req['log'])
                return MessageAdmin.get_on_going_message()
            else:
                fail_message = MessageAdmin.get_fail_message()
                fail_message.update_message(req['log'])
                return fail_message


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
