from .message import HomeMessage, FailMessage

class Singleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class APIManager(metaclass=Singleton):
    def process(self, status, message=None):
        if status is 'home':
            home_message = MessageAdmin.get_home_message()
            return home_message
        elif status is 'food':
            pass
        elif status is 'bus':
            pass
        elif status is 'library':
            pass
        elif status is 'subway':
            pass
        elif status is 'fail':
            fail_message = MessageAdmin.get_fail_message()
            return fail_message
        else:
            fail_message = MessageAdmin.get_fail_message()
            return fail_message

class MessageManager(metaclass=Singleton):
    def get_home_message(self):
        return HomeMessage()

    def get_fail_message(self):
        return FailMessage()


class KeyboardManager(metaclass=Singleton):
    pass

APIAdmin = APIManager()
MessageAdmin = MessageManager()
