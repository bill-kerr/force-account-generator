from hours import Hours


class Equipment:
    def __init__(self):
        self.description = ""
        self.year = ""
        self.type = ""
        self.configuration = ""
        self.make = ""
        self.model = ""
        self.equipment_number = ""
        self.h_yr = ""
        self.sec_pg = ""
        self.monthly_rate = 0
        self.equipment_adjustment = 0
        self.area_adjustment = 0
        self.operating_cost = 0
        self.__daily_hours = {}

    @property
    def daily_hours(self):
        return self.__daily_hours

    def add_daily_hours(self, date, operating_time, standby_time):
        hours = Hours(date, operating_time, standby_time)
        self.__daily_hours[date] = hours
