import datetime
import time

a = time.mktime(datetime.date(2020, 1, 1).timetuple())
b = datetime.date.fromtimestamp(a).isocalendar()
print(b)
print(a)