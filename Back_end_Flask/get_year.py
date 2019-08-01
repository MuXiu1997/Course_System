import datetime
import json
import time

import requests


def get_workday(year):
    year_dict = dict()
    start_date = datetime.date(year, 1, 1)
    start_date_timetuple = time.mktime(start_date.timetuple())
    _date = start_date_timetuple

    while True:
        day = datetime.date.fromtimestamp(_date)
        year_dict[day.isoformat()] = day.weekday() < 5
        _date += 24 * 60 * 60
        if day.isoformat().split('-')[0] != str(year):
            return year_dict


def get_workday_api(year):
    url = 'http://www.mxnzp.com/api/holiday/list/year/%s' % year
    request_api_text = requests.get(url).text
    request_api_json = json.loads(request_api_text)

    if not request_api_json.get('code'):
        return get_workday(year)

    year_dict = dict()
    for each_month in request_api_json['data']:
        for each_day in each_month['days']:
            year_dict[each_day['date']] = each_day['typeDes'] == '工作日'

    return year_dict


def run(year):
    year_dict = dict()
    for i in range(5):
        year_dict = dict(year_dict, **get_workday_api(year + i))

    with open('workday_data.json', 'w', encoding='utf8') as api_file_obj:
        json.dump(year_dict, api_file_obj, ensure_ascii=False)


if __name__ == '__main__':
    start_year = int(input('输入起始年份：'))
    run(start_year)
