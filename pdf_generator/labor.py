from hours import Hours


class Labor:
    def __init__(self):
        self.classification = ""
        self.name = ""
        self.base_rate = 0
        self.hw_pension_rate = 0
        self.__daily_hours = []

    @property
    def daily_hours(self):
        return self.__daily_hours

    def add_daily_hours(self, date, straight_time, overtime):
        hours = Hours(date, straight_time, overtime)
        self.__daily_hours.append(hours)
