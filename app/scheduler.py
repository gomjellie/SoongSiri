import schedule
import threading
from time import sleep
from .parser import food_api
from .myLogger import viewLog
import datetime
from .managers import DBManager


class MenuFetcher(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        schedule.clear()
        schedule.every().day.at("05:30").do(self.fetch_save_menu).tag('first-attempt')

    def run(self):
        while True:
            schedule.run_pending()
            sleep(60)

    def fetch_save_menu(self):
        def set_rate(f_dicts):
            for f_dict in f_dicts:
                for sec in f_dict:
                    f_dict[sec].update({
                        '평점': 0,
                        '참여자': [],
                    })
        try:
            if DBManager.get_data():
                viewLog("fail", '오늘의 데이터는 이미 저장되어 있습니다.')
                return
            food_api.refresh()
            food_court = food_api.get_food_court()
            faculty_food = food_api.get_faculty_food()
            pupil_food = food_api.get_pupil_food()
            dorm_foods = food_api.get_dormitory_food()
            day_of_week = datetime.datetime.today().weekday()
            dorm_food = dorm_foods.get(' 월화수목금토일'[day_of_week])
            date = datetime.date.today().__str__()

            ratable_list = [faculty_food, pupil_food, dorm_food]
            set_rate(ratable_list)
            food_dict = {
                '푸드코트': food_court,
                '학식': pupil_food,
                '교식': faculty_food,
                '기식': dorm_food,
                '날짜': date,
            }
            viewLog('scheduler', food_dict)
            DBManager.set_data(food_dict)

        except Exception as inst:
            viewLog("fail", inst.__str__())
            schedule.clear('second-attempt')
            schedule.every().day.at("09:00").do(self.fetch_save_menu).tag('second-attempt')


menu_scheduler = MenuFetcher()
