import datetime
from .myLogger import viewLog
from .managers import DBAdmin


class Review:
    def __init__(self):
        pass

    @staticmethod
    def get_string():
        """
        get today's reviews which contains converted user_key and review string
        :return: string
        example: "dreNXN: 솰라솰라\nkkp02n: 뭐라뭐라뭐라"
        """
        reviews = DBAdmin.get_review()
        ret = '{}\n'.format(datetime.date.today().__str__())

        if not reviews:
            Review.init_today_review()
            ret = '오늘은 리뷰가 아직 없습니다.' + \
                  '\n리뷰를 처음으로 남겨 보세요'

        for review in reviews:
            user_key = list(review)[0]
            msg = review[user_key]
            shorten_user_key = user_key[:3] + user_key[-3:]
            ret += "\n{}: {}".format(shorten_user_key, msg)

        return ret

    @staticmethod
    def new_review(user_key, new_review):
        viewLog("review", {'user_key': user_key, 'review': new_review})
        DBAdmin.append_review(user_key, new_review)

    @staticmethod
    def init_today_review():
        if not DBAdmin.get_review():
            DBAdmin.init_review()
