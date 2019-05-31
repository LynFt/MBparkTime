from datetime import datetime, timedelta
from dateutil import relativedelta


class DateUtils:
    def get_week_day(self, datestr):
        week_day_dict = {
            0: '星期一',
            1: '星期二',
            2: '星期三',
            3: '星期四',
            4: '星期五',
            5: '星期六',
            6: '星期天',
        }
        date = datetime.strptime(datestr, "%Y-%m-%d")
        day = date.weekday()
        return week_day_dict[day]
    
    def get_month_date(self, year, moth):
        now = datetime(year, moth, 1)
        delta = timedelta(days=1)
        date_list = []
        while now.month == moth:
            date_list.append(now.strftime("%Y-%m-%d"))
            now = now + delta
        return date_list
    
    def get_next_month(self):
        now = datetime.now()
        month = now.month + 1
        year = now.year
        if month > 12:
            month = 1
            year += 1
        now = datetime(year=year, month=month, day=1)
        return now
    
    def get_before_month(self):
        now = datetime.now()
        month = now.month - 1
        year = now.year
        if month < 1:
            month = 12
            year -= 1
        now = datetime(year=year, month=month, day=1)
        return now
