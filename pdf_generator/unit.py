class Hours:
    def __init__(self, date, primary_hours, secondary_hours):
        self.date = date
        self.primary_hours = primary_hours
        self.secondary_hours = secondary_hours

    def __repr__(self):
        return "Hours(" + self.date + ", " + str(self.primary_hours or 0) + "/" + str(self.secondary_hours or 0) + ")"


class Unit:
    def __init__(self):
        self.daily_hours = {}

    def add_daily_hours(self, date, primary_hours, secondary_hours):
        hours = Hours(date, primary_hours, secondary_hours)
        self.daily_hours[date] = hours

    def get_total_hours(self, secondary=False):
        total_hours = 0
        for hours in self.daily_hours.values():
            total_hours += (hours.primary_hours or 0) if not secondary else (hours.secondary_hours or 0)
        return total_hours
