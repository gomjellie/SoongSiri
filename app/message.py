from .keyboard import Keyboard
from json import loads, dumps
from .menu import PupilMenu, FacultyMenu
from .parser import subway_api, bus_api
from .library_seat import LibrarySeat

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
        self.update_keyboard(Keyboard.home_buttons)


class FacultyFoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        f = FacultyMenu()
        f.set_faculty_foods()
        self.update_message(f.get_string())
        self.update_keyboard(Keyboard.home_buttons)


class HomeMessage(Message):
    def __init__(self):
        self.retMessage = Message.baseKeyboard
        homeKeyboard = Keyboard.home_buttons
        self.retMessage['buttons'] = homeKeyboard


class BusMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        self.update_message('버스 정류장을 선택해 주세요')
        self.update_keyboard(Keyboard.bus_buttons)

    def bera(self):
        bera_msg = bus_api.get_station_stat('20165')
        self.update_message(bera_msg)
        self.update_keyboard(Keyboard.home_buttons)

    def front(self):
        front_msg = bus_api.get_station_stat('')
        self.update_message(front_msg)
        self.update_keyboard(Keyboard.home_buttons)

    def middle(self):
        mid_msg = bus_api.get_station_stat('')
        self.update_message(mid_msg)
        self.update_keyboard(Keyboard.home_buttons)


class LibMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        l = LibrarySeat()
        self.update_message('열람실을 선택해 주세요')
        self.update_keyboard(l.get_buttons())


class SubMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        sub_msg = subway_api.get_station_stat('숭실대입구')
        self.update_message(sub_msg)


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
