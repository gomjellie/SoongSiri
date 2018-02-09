from .keyboard import Keyboard
from json import loads, dumps
from .menu import pupil_menu, faculty_menu, food_court_menu,\
    dormitory_menu, the_kitchen_menu, snack_corner_menu
from .parser import subway_api, bus_api
from .library_seat import LibrarySeat
from .review import Review
from .constants import get_timetable_string
import datetime


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


class KeyboardMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        del self.retMessage['keyboard']

    def get_message(self):
        return self.retMessage

    def update_message(self, message):
        self.retMessage['message']['text'] = message

    def update_keyboard(self, keyboard):
        raise Exception("don't use update_keyboard function")


class CancelMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        self.update_message('취소되었습니다')
        self.update_keyboard(Keyboard.home_buttons)


class FoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        self.update_message('장소를 선택해주세요\n\n오른쪽으로 스와이프 하면 버튼 더 있어요.\n오른쪽에 공간있어요')
        self.update_keyboard(Keyboard.food_buttons)


class TomorrowFoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        if datetime.date.today().weekday() == 6:
            self.update_message('일요일은 내일의 식단을 볼 수 없습니다.')
            self.update_keyboard(['취소'])
        else:
            self.update_message('장소를 선택해주세요')
            self.update_keyboard(Keyboard.food_buttons)


class PupilFoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        pupil_menu.prepare_food()
        open_time = get_timetable_string('학식')
        self.update_message(pupil_menu.get_string() + open_time)
        self.update_keyboard(Keyboard.home_buttons)


class TomorrowPupilFoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        date = datetime.date.today() + datetime.timedelta(days=1)
        pupil_menu.prepare_food(date)
        open_time = get_timetable_string('학식', '내일')
        self.update_message(pupil_menu.get_string(date) + open_time)
        self.update_keyboard(Keyboard.home_buttons)


class FacultyFoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        faculty_menu.prepare_food()
        open_time = get_timetable_string('교식')
        self.update_message(faculty_menu.get_string() + open_time)
        self.update_keyboard(Keyboard.home_buttons)


class TomorrowFacultyFoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        date = datetime.date.today() + datetime.timedelta(days=1)
        faculty_menu.prepare_food(date)
        open_time = get_timetable_string('교식', '내일')
        self.update_message(faculty_menu.get_string(date) + open_time)
        self.update_keyboard(Keyboard.home_buttons)


class FoodCourtMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        food_court_menu.prepare_food()
        open_time = get_timetable_string('푸드코트')
        self.update_message(food_court_menu.get_string() + open_time)
        self.update_keyboard(Keyboard.home_buttons)


class TomorrowFoodCourtMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        date = datetime.date.today() + datetime.timedelta(days=1)
        food_court_menu.prepare_food(date)
        open_time = get_timetable_string('푸드코트', '내일')
        self.update_message(food_court_menu.get_string(date) + open_time)
        self.update_keyboard(Keyboard.home_buttons)


class TheKitchenMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        the_kitchen_menu.prepare_food()
        open_time = get_timetable_string('더 키친')
        self.update_message(the_kitchen_menu.get_string() + open_time)
        self.update_keyboard(Keyboard.home_buttons)


class TomorrowTheKitchenMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        date = datetime.date.today() + datetime.timedelta(days=1)
        the_kitchen_menu.prepare_food(date)
        open_time = get_timetable_string('더 키친', '내일')
        self.update_message(the_kitchen_menu.get_string(date) + open_time)
        self.update_keyboard(Keyboard.home_buttons)


class SnackCornerMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        snack_corner_menu.prepare_food()
        open_time = get_timetable_string('스넥코너')
        self.update_message(snack_corner_menu.get_string() + open_time)
        self.update_keyboard(Keyboard.home_buttons)


class TomorrowSnackCornerMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        date = datetime.date.today() + datetime.timedelta(days=1)
        snack_corner_menu.prepare_food(date)
        open_time = get_timetable_string('스넥코너', '내일')
        self.update_message(snack_corner_menu.get_string(date) + open_time)
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


class TomorrowDormFoodMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        date = datetime.date.today() + datetime.timedelta(days=1)
        dormitory_menu.prepare_food(date)
        open_time = '\n조식 : 08:00 ~ 09:30' +\
                    '\n중식 : 11:00 ~ 14:00' +\
                    '\n석식 : 17:00 ~ 18:30' +\
                    '\n쉬는시간 : 14:30~15:00 16:00~17:00'
        self.update_message(dormitory_menu.get_string(date) + open_time)
        self.update_keyboard(Keyboard.home_buttons)


class SelectFoodPlaceMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        self.update_message('평가할 장소를 선택해주세요')
        self.update_keyboard(Keyboard.ratable_food_buttons)


class ReviewInitMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        self.update_message('리뷰를 참고하거나, 리뷰를 직접 남겨보세요.')
        self.update_keyboard(Keyboard.review_buttons)


class ReviewPostMessage(KeyboardMessage):
    def __init__(self):
        super().__init__()
        self.update_message('욕설, 타인을 비방하는 내용이 포함될 경우,' +
                            '\n2018년 7월 4일까지 해당기능을 이용하실 수 없습니다.' +
                            "\n'취소'를 입력 하시면 취소 할 수 있습니다.")


class ReviewBrowseMessage(BaseMessage):
    def __init__(self):
        super().__init__()
        self.update_message(Review.get_string())
        self.update_keyboard(Keyboard.home_buttons)


class ReviewPostSuccess(BaseMessage):
    def __init__(self, user_key, content):
        super().__init__()
        Review.new_review(user_key, content)
        self.update_message('성공적으로 등록되었습니다.')
        self.update_keyboard(Keyboard.home_buttons)


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
            self.update_message("해당 음식은 {} ~ {}에만 평가 할 수 있습니다.".format(
                start_time.strftime("%H:%M"), end_time.strftime("%H:%M")))
        self.update_keyboard(Keyboard.home_buttons)


class RateFoodEndMessage(BaseMessage):
    def __init__(self, prev, post):
        super().__init__()
        self.update_message("{:0.2f}에서 {:0.2f}으로 별점이 변경되었습니다.".format(prev, post))
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


class TimeTableMessage(UrlMessage):
    def __init__(self):
        super().__init__()
        url = 'http://soongguri.com/pages/hours.php'
        self.update_message('방학중 생활협동조합 매장별 운영시간', '매장별 시간 확인하기', url)


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

