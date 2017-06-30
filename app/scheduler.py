import schedule
import datetime
import time
import threading
from .parser import FoodParser
from app import hakusiku
from .myLogger import viewLog


class MenuFetcher(threading.Thread):
    """
    작동확인 못함
    """
    def __init__(self):
        super().__init__()
        self.scheduled_time = "00:02"
        schedule.every().day.at(self.scheduled_time).do(self.fetch_save_menu)

    def run(self):
        schedule.run_pending()
        time.sleep(60)

    def fetch_save_menu(self):
        f = FoodParser()
        try:
            f.refresh()
            food_court = f.get_food_court()
            faculty_food = f.get_faculty_food()
            pupil_food = f.get_pupil_food()
            date = datetime.datetime.now().date().__str__()
            food_dict = {
                '푸드코트': food_court,
                '학식': pupil_food,
                '교식': faculty_food,
                '날짜': date,
                '평점': 0,
                '참여자': []
            }
            viewLog('scheduler', food_dict)
            hakusiku.insert(food_dict)

        except Exception as inst:
            viewLog("fail", inst.__str__())
            self.scheduled_time = "06:00"
            schedule.every().day.at(self.scheduled_time).do(self.fetch_save_menu)


menu_scheduler = MenuFetcher()
