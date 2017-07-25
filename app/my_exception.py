

class FoodNotFound(Exception):
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return "식단을 불러올 수 없습니다.\n {}".format(self.msg)


class FoodRateDuplicate(Exception):
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return "이미 평가한 항목입니다.\n {}".format(self.msg)

