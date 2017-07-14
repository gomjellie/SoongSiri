from .keyboard import Keyboard
from json import loads, dumps
from .menu import PupilMenu, FacultyMenu, FoodCourtMenu
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
        p.set_food()
        self.update_message(p.get_string())
        self.update_keyboard(Keyboard.home_buttons)


class FacultyFoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        f = FacultyMenu()
        f.set_food()
        self.update_message(f.get_string())
        self.update_keyboard(Keyboard.home_buttons)


class FoodCourtMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        f = FoodCourtMenu()
        f.set_food()
        self.update_message(f.get_string())
        self.update_keyboard(Keyboard.home_buttons)


class RatingFoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        self.update_message('평가할 장소를 선택해주세요')
        self.update_keyboard(Keyboard.food_buttons)


class RatingPupilMessage(BaseMessage):
    def __init__(self):
        p = PupilMenu()
        p.set_food()
        time = p.get_times()
        self.update_message('평가할 식단을 선택해 주세요\n' + p.get_string())
        self.update_keyboard(time)


class RatingFacultyMessage(BaseMessage):
    def __init__(self):
        f = FacultyMenu()
        f.set_food()
        time = f.get_times()
        self.update_message('평가할 식단을 선택해 주세요\n' + f.get_string())
        self.update_keyboard(time)


class RatingFoodCourtMessage(BaseMessage):
    def __init__(self):
        fc = FoodCourtMenu()
        fc.set_food()
        time = fc.get_times()
        self.update_message('평가할 식단을 선택해 주세요\n' + fc.get_string())
        self.update_keyboard(time)


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


class BusBeraMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        bera_msg = bus_api.get_station_stat('20165')
        self.update_message(bera_msg)
        self.update_keyboard(Keyboard.home_buttons)


class BusFrontMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        front_msg = bus_api.get_station_stat('20166')
        self.update_message(front_msg)
        self.update_keyboard(Keyboard.home_buttons)


class BusMiddleMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        mid_msg = bus_api.get_station_stat('20169')
        self.update_message(mid_msg)
        self.update_keyboard(Keyboard.home_buttons)


class LibMessage(BaseMessage):
    def __init__(self, room=None):
        super().__init__()
        if room:
            self.update_message('http://203.253.28.47/seat/roomview5.asp?room_no={}'.format(room))
            self.update_keyboard(Keyboard.home_buttons)
        else:
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

