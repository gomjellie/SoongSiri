import datetime
from .myLogger import viewLog


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
        from .managers import DBAdmin
        reviews = DBAdmin.get_review()['리뷰']
        ret = '{}\n'.format(datetime.date.today().__str__())

        if not reviews:
            ret = '오늘은 리뷰가 아직 없습니다.' + \
                  '\n리뷰를 처음으로 남겨 보세요'

        for review in reviews:
            user_key = review['user_key']
            msg = review['content']
            shorten_user_key = user_key[:3] + user_key[-3:]
            ret += "\n{}: {}".format(shorten_user_key, msg)

        return ret

    @staticmethod
    def new_review(user_key, new_review):
        from .managers import DBAdmin
        if DBAdmin.is_banned_user(user_key):
            raise Exception('Banned User')
        viewLog("review", {'user_key': user_key, 'content': new_review})
        DBAdmin.append_review(user_key, new_review)

    @staticmethod
    def remove_current_review(user_key):
        from .managers import DBAdmin
        reviews = DBAdmin.get_review()['리뷰']
        for review in reviews[::-1]:
            if review['user_key'] == user_key:
                reviews.pop(review)
                DBAdmin.review.find_one_and_replace({'날짜': datetime.date.today().__str__()}, reviews)
                return
