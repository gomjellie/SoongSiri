from .keyboard import Keyboard
from json import loads, dumps
from .menu import pupil_menu, faculty_menu, food_court_menu
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
        pupil_menu.fetch_food()
        open_time = '평일 :   10:30 ~ 14:00(중식)\n주말 :   운영안함'
        self.update_message(pupil_menu.get_string() + open_time)
        self.update_keyboard(Keyboard.home_buttons)


class FacultyFoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        faculty_menu.fetch_food()
        open_time = '평일 :   11:30 ~ 14:00(중식)' +\
                    '평일 :   17:00 ~ 18:10(중식)' +\
                    '주말 :   11:30 ~ 14:00(중식)'
        self.update_message(faculty_menu.get_string() + open_time)
        self.update_keyboard(Keyboard.home_buttons)


class FoodCourtMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        food_court_menu.fetch_food()
        open_time = '평일 :   11:00 ~ 15:00(중식)' +\
                    '주말 :   운영안함'
        self.update_message(food_court_menu.get_string() + open_time)
        self.update_keyboard(Keyboard.home_buttons)


class SelectFoodPlaceMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        self.update_message('평가할 장소를 선택해주세요')
        self.update_keyboard(Keyboard.ratable_food_buttons)


class RatingPupilMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        pupil_menu.fetch_food()
        time = pupil_menu.get_times()
        self.update_message('평가할 식단을 선택해 주세요\n' + pupil_menu.get_string())
        self.update_keyboard(time)


class RatingFacultyMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        faculty_menu.fetch_food()
        time = faculty_menu.get_times()
        self.update_message('평가할 식단을 선택해 주세요\n' + faculty_menu.get_string())
        self.update_keyboard(time)


class RatingFoodCourtMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        food_court_menu.fetch_food()
        time = food_court_menu.get_times()
        self.update_message('평가할 식단을 선택해 주세요\n' + food_court_menu.get_string())
        self.update_keyboard(time)


class RateFoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        self.update_message('맛을 평가해 주세요')
        self.update_keyboard(Keyboard.rating_buttons)


class RateFoodEndMessage(BaseMessage):
    def __init__(self, prev, next):
        super().__init__()
        self.update_message("{}에서 {}으로 평점이 변경되었습니다.".format(prev, next))
        self.update_keyboard(Keyboard.home_buttons)


class HomeMessage(Message):
    def __init__(self):
        super().__init__()
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
            self.update_message('열람실을 선택해 주세요')
            self.update_keyboard(LibrarySeat.get_buttons())


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

