from .keyboard import Keyboard
from json import loads, dumps
from .menu import pupil_menu, faculty_menu, food_court_menu, dormitory_menu
from .parser import subway_api, bus_api
from .library_seat import LibrarySeat


class SuccessMessage:
    @staticmethod
    def get_message():
        return {"message": "SUCCESS"}


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
        if '취소' not in kb['buttons']:
            kb['buttons'].append('취소')
        self.retMessage['keyboard'] = kb


class UrlMessage(BaseMessage):
    def __init__(self):
        super().__init__()

    def update_message(self, text, label, url):
        message_button = {
            'label': label,
            'url': url,
        }
        self.retMessage['message']['text'] = text
        self.retMessage['message'].update({'message_button': message_button})


class CancelMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        self.update_message('취소되었습니다')
        self.update_keyboard(Keyboard.home_buttons)


class FoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        self.update_message('장소를 선택해주세요')
        self.update_keyboard(Keyboard.food_buttons)


class PupilFoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        pupil_menu.prepare_food()
        open_time = '\n평일 :   10:30 ~ 14:00(중식)\n주말 :   운영안함'
        self.update_message(pupil_menu.get_string() + open_time)
        self.update_keyboard(Keyboard.home_buttons)


class FacultyFoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        faculty_menu.prepare_food()
        open_time = '\n평일 :   11:30 ~ 14:00(중식)' +\
                    '\n평일 :   17:00 ~ 18:10(석식)' +\
                    '\n주말 :   11:30 ~ 14:00(중식)'
        self.update_message(faculty_menu.get_string() + open_time)
        self.update_keyboard(Keyboard.home_buttons)


class FoodCourtMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        food_court_menu.prepare_food()
        open_time = '\n평일 :   11:00 ~ 15:00(중식)' +\
                    '\n주말 :   운영안함'
        self.update_message(food_court_menu.get_string() + open_time)
        self.update_keyboard(Keyboard.home_buttons)


class DormFoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        dormitory_menu.prepare_food()
        open_time = '\n조식 : 08:00 ~ 09:30' +\
                    '\n중식 : 11:00 ~ 14:00' +\
                    '\n석식 : 17:00 ~ 18:30' +\
                    '\n쉬는시간 : 14:30~15:00 16:00~17:00'
        self.update_message(dormitory_menu.get_string() + open_time)
        self.update_keyboard(Keyboard.home_buttons)


class SelectFoodPlaceMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        self.update_message('평가할 장소를 선택해주세요')
        self.update_keyboard(Keyboard.ratable_food_buttons)


class RatingPupilMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        pupil_menu.prepare_food()
        time = pupil_menu.get_times()
        self.update_message('평가할 식단을 선택해 주세요\n' + pupil_menu.get_string())
        self.update_keyboard(time)


class RatingFacultyMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        faculty_menu.prepare_food()
        time = faculty_menu.get_times()
        self.update_message('평가할 식단을 선택해 주세요\n' + faculty_menu.get_string())
        self.update_keyboard(time)


class RatingFoodCourtMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        food_court_menu.prepare_food()
        time = food_court_menu.get_times()
        self.update_message('평가할 식단을 선택해 주세요\n' + food_court_menu.get_string())
        self.update_keyboard(time)


class RatingDormFoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        dormitory_menu.prepare_food()
        time = dormitory_menu.get_times()
        self.update_message('평가할 식단을 선택해 주세요\n' + dormitory_menu.get_string())
        self.update_keyboard(time)


class RateFoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        self.update_message('맛을 평가해 주세요')
        self.update_keyboard(Keyboard.rating_buttons)


class FoodNonVotableMessage(BaseMessage):
    def __init__(self, start_time, end_time):
        super().__init__()
        if start_time == end_time:
            self.update_message("해당음식은 오늘 서비스 되지 않아서 평가 할 수 없습니다.")
        else:
            self.update_message("해당 음식은 {} ~ {}에만 평가 할 수 있습니다.".format(start_time, end_time))
        self.update_keyboard(Keyboard.home_buttons)


class RateFoodEndMessage(BaseMessage):
    def __init__(self, prev, post):
        super().__init__()
        self.update_message("{:0.2f}에서 {:0.2f}으로 평점이 변경되었습니다.".format(prev, post))
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
    def __init__(self):
        super().__init__()
        self.update_message('열람실을 선택해 주세요')
        self.update_keyboard(LibrarySeat.get_buttons())


class LibStatMessage(UrlMessage):
    def __init__(self, room):
        super().__init__()
        url = 'http://203.253.28.47/seat/roomview5.asp?room_no={}'.format(room)
        self.update_message('{}열람실 좌석 테이블입니다.'.format(room), '좌석 확인하기', url)
        self.update_keyboard(Keyboard.home_buttons)


class SubMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        sub_msg = subway_api.get_station_stat('숭실대입구')
        self.update_message(sub_msg)


class FailMessage(BaseMessage):
    def __init__(self, msg=None):
        super().__init__()
        self.update_message('에러가 발생했습니다.\nmsg: ' + msg)
        self.update_keyboard(Keyboard.home_buttons)


class OnGoingMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        self.update_message('만드는 중입니다.')
        self.update_keyboard(Keyboard.home_buttons)

