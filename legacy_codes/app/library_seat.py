from .parser import lib_api
from collections import OrderedDict


class LibrarySeat:
    @staticmethod
    def get_buttons():
        ret_buttons = []
        unordered_lib_stats = lib_api.get_lib_stat()
        lib_stats = OrderedDict(sorted(unordered_lib_stats.items()))
        for button in lib_stats:
            button_text = button + ' (이용률 :' + lib_stats[button]['이용률'] + ')'
            ret_buttons.append(button_text)

        return ret_buttons
