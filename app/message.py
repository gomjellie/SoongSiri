from .keyboard import Keyboard
from json import loads, dumps


class Message:
    baseKeyboard = {
        "type": "buttons",
        "buttons": Keyboard.buttons
    }

    baseMessage = {
        "message": {
            "text": "",
        },
        "keyboard": baseKeyboard
    }

    def __init__(self):
        self.retMessage = None

    def get_message(self):
        return self.retMessage


class BaseMessage(Message):
    def __init__(self):
        super().__init__()
        self.retMessage = loads(dumps(Message.baseMessage))

    def update_message(self, message):
        self.retMessage['message']['text'] = message

    def update_keyboard(self, keyboard):
        kb = Message.baseKeyboard
        kb['buttons'] = keyboard
        self.retMessage['keyboard'] = kb


class FoodMessage(BaseMessage):
    def __init__(self):
        self.retMessage = Message.baseKeyboard
        self.update_keyboard(Keyboard.food_buttons)


class HomeMessage(Message):
    def __init__(self):
        self.retMessage = Message.baseKeyboard
        homeKeyboard = Keyboard.home_buttons
        self.retMessage['buttons'] = homeKeyboard


class FailMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        self.update_message('error occured')
        self.update_keyboard(Keyboard.home_buttons)