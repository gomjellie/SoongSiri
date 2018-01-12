
time_table = {
    '학식': {
        '평일': ['10:30 ~ 14:00(중식)'],
        '주말': ['방학중 휴무'],
    },
    '교식': {
        '평일': [
            '11:20 ~ 14:00(중식)',
            '17:00 ~ 18:10(석식)',
        ],
        '주말': ['11:20 ~ 14:00(중식)'],
    },
    '푸드코트': {
        '평일': ['방학중 휴무'],
        '주말': ['방학중 휴무'],
    },
    '스넥코너': {
        '평일': ['방학중 휴무'],
        '주말': ['방학중 휴무'],
    },
    '더 키친': {
        '평일': ['방학중 휴무'],
        '주말': ['방학중 휴무'],
    }
}


def get_timetable_string(location):
    t = time_table[location]
    ret = ''
    look_up_order = '평일 주말'.split()
    for day in look_up_order:
        if day in t:
            day_time = t[day]
            for time in day_time:
                ret += '\n{} :   {}'.format(day, time)

    return ret
