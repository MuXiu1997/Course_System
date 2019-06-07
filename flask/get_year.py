import datetime
import json
import time


def get_workday(year):
    year_dict = dict()
    start_date = datetime.date(year, 1, 1)
    start_date_timetuple = time.mktime(start_date.timetuple())
    _date = start_date_timetuple
    while datetime.date.fromtimestamp(_date).isocalendar()[0] == year:
        day = datetime.date.fromtimestamp(_date)
        year_dict[str(day)] = day.weekday() < 5
        _date += 24 * 60 * 60
    return year_dict


a = (get_workday(2020))
with open('a.json', 'w', encoding='utf8') as api_file_obj:
    json.dump(a, api_file_obj, ensure_ascii=False)
