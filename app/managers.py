from .message import HomeMessage, FailMessage, FoodMessage


class Singleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class APIManager(metaclass=Singleton):
    def process(self, req, message=None):
        if req is 'home':
            home_message = MessageAdmin.get_home_message()
            return home_message
        elif req is 'food':
            return MessageAdmin.get_food_message()
        elif req is 'bus':
            pass
        elif req is 'library':
            pass
        elif req is 'subway':
            pass
        elif req is 'fail':
            fail_message = MessageAdmin.get_fail_message()
            return fail_message
        else:
            fail_message = MessageAdmin.get_fail_message()
            return fail_message


class MessageManager(metaclass=Singleton):
    def get_home_message(self):
        return HomeMessage()

    def get_food_message(self):
        return FoodMessage()

    def get_fail_message(self):
        return FailMessage()


class KeyboardManager(metaclass=Singleton):
    pass

APIAdmin = APIManager()
MessageAdmin = MessageManager()
