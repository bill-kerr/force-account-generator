class WorkDay:
    def __init__(self, unit, date):
        self.date = date
        self.primary_hours = unit.daily_hours.get(date).primary_hours
        self.secondary_hours = unit.daily_hours.get(date).secondary_hours

    def __repr__(self):
        return "WorkDay(" + str(self.primary_hours) + ", " + str(self.secondary_hours) + ")"
