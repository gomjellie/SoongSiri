import schedule
import datetime
import threading
from time import sleep
from .parser import food_api
from app import hakusiku
from .myLogger import viewLog
import datetime


class MenuFetcher(threading.Thread):
    """
    SoongsilFood.log 에
    2017-07-04 00:02:35,588-[parsing] 학식: {'중식1': ['돈가스오므라이스', '크림치즈샐러드']}, 교식: {'조식': ['방중', '미운영'], '중식1': ['집밥정식', '가자비구이', '올갱이상청양된장찌개', '보리비빔밥고추장볶음', '계란찜', '콩자반', '낙지젓갈무침', '열무김치', '냉미숫가루'], '석식1': ['무항생제통등심일식돈까스소스', '새송이도라지초장무침', '양상추샐러드드레싱']}, 푸드코트: {'메뉴': ['삼선짬뽕 6.0', '소고기마파두부6.0', '치킨마늘볶음밥 6.0', '로스까스 6.5', '삼선짬뽕밥 6.0', '퓨전소고기마파두부6.0', '팟타이볶음쌀국수 6.5', '찜닭공기밥 6.5', '연어회덮밥 7.0']}, 날짜: 2017-07-04
    2017-07-04 00:02:41,095-[parsing] 학식: {'중식1': ['돈가스오므라이스', '크림치즈샐러드']}, 교식: {'조식': ['방중', '미운영'], '중식1': ['집밥정식', '가자비구이', '올갱이상청양된장찌개', '보리비빔밥고추장볶음', '계란찜', '콩자반', '낙지젓갈무침', '열무김치', '냉미숫가루'], '석식1': ['무항생제통등심일식돈까스소스', '새송이도라지초장무침', '양상추샐러드드레싱']}, 푸드코트: {'메뉴': ['찜닭공기밥 6.5', '로스까스 6.5', '치킨마늘볶음밥 6.0', '팟타이볶음쌀국수 6.5', '퓨전소고기마파두부6.0', '삼선짬뽕 6.0', '삼선짬뽕밥 6.0', '연어회덮밥 7.0', '소고기마파두부6.0']}, 날짜: 2017-07-04
    이렇게 2번 파싱한 흔적이 있고
    hakusiku db에 7월 04일 메뉴 똑같은게 5개가 중복되서 저장되있음
    """
    def __init__(self):
        super().__init__()
        self.daemon = True
        schedule.clear()    # 혹시 스케쥴러가 여러개 돌고있을지도 모르니까 한번 추가해봄
        schedule.every().day.at("00:02").do(self.fetch_save_menu).tag('first-attempt')

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
            today = datetime.datetime.today().__str__()
            if hakusiku.find_one({'날짜': today}):
                viewLog("fail", '오늘의 데이터는 이미 저장되어 있습니다.')
                return
            food_api.refresh()
            food_court = food_api.get_food_court()
            faculty_food = food_api.get_faculty_food()
            pupil_food = food_api.get_pupil_food()
            date = datetime.datetime.now().date().__str__()

            ratable_list = [faculty_food, pupil_food]
            set_rate(ratable_list)
            food_dict = {
                '푸드코트': food_court,
                '학식': pupil_food,
                '교식': faculty_food,
                '날짜': date,
            }
            viewLog('scheduler', food_dict)
            if not hakusiku.find_one(food_dict):
                hakusiku.insert_one(food_dict)

        except Exception as inst:
            viewLog("fail", inst.__str__())
            schedule.clear('second-attempt')
            schedule.every().day.at("06:00").do(self.fetch_save_menu).tag('second-attempt')


menu_scheduler = MenuFetcher()
