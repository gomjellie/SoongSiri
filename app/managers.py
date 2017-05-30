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
            if content == u'밥':
                print('food')
                return MessageAdmin.get_food_message()
            elif content in ['학식', '교식']:
                if content == '학식':
                    return PupilFoodMessage()
                elif content == '교식':
                    return FacultyFoodMessage()
            elif content is '버스':
                return BusMessage()
            elif content is '도서관':
                return LibMessage
            elif content is '지하철':
                return SubMessage
            elif content is 'fail':
                fail_message = MessageAdmin.get_fail_message()
                return fail_message
            else:
                return MessageAdmin.get_on_going_message()


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
