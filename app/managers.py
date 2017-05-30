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
        else:
            content = req['content']
            if content is '학식':
                return MessageAdmin.get_food_message()
            elif content is 'bus':
                pass
            elif content is 'library':
                pass
            elif content is 'subway':
                pass
            elif content is 'fail':
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
