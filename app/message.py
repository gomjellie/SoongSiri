from .keyboard import Keyboard
from json import loads, dumps
from .menu import PupilMenu, FacultyMenu

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
        super().__init__()
        self.update_message('장소를 선택해주세요')
        self.update_keyboard(Keyboard.food_buttons)


class PupilFoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        p = PupilMenu()
        p.set_pupil_foods()
        self.update_message(p.get_string())


class FacultyFoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        f = FacultyMenu()
        f.set_faculty_foods()
        self.update_message(f.get_string())

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

class OnGoingMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        self.update_message('만드는 중입니다.')
        self.update_keyboard(Keyboard.home_buttons)
