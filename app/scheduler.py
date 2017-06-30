import schedule
import datetime
import threading
from .parser import FoodParser
from app import hakusiku
from .myLogger import viewLog


class MenuFetcher(threading.Thread):
    def __init__(self):
        self.scheduled_time = "00:02"

    def run(self):
        schedule.every().day.at(self.scheduled_time).do(self.fetch_save_menu)

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
            self.scheduled_time = "06:00"


menu_scheduler = MenuFetcher(name='MenuFetcher')
