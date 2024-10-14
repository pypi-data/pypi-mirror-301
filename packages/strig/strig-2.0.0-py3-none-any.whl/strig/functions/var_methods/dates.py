from datetime import datetime
from typing import Optional


class DateMethods:
    today = datetime.today()

    def yyyy(self):
        return self.today.year

    def yy(self):
        return str(self.today.year)[-2:]

    def mm(self):
        month = str(self.today.month)
        if len(month) == 2:
            return month
        return "0" + month

    def m(self):
        return self.today.month

    def month_name(self):
        return self.today.strftime("%B")

    def month_short(self):
        return self.today.strftime("%b")

    def dd(self):
        day = str(self.today.day)
        if len(day) == 2:
            return day
        return "0" + day

    def d(self):
        return self.today.day

    def weekday_name(self):
        return self.today.strftime("%A")

    def w(self):
        return self.today.weekday()

    def week(self):
        return self.today.isocalendar()[1]

    def day_of_year(self):
        return self.today.timetuple().tm_yday

    def ampm(self):
        return self.today.strftime("%p")

    def hh(self):
        return self.today.strftime("%H")

    def h(self):
        return self.today.hour

    def minute(self):
        return self.today.strftime("%M")

    def quarter(self):
        return (self.today.month - 1) // 3 + 1

    def timestamp(self):
        return int(self.today.timestamp())
