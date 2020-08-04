from work_day import WorkDay


def add_unit_days(unit, collection):
    for day in unit.daily_hours.values():
        work_day = WorkDay(unit, day.date)
        if collection.get(day.date) is None:
            collection[day.date] = [work_day]
        else:
            collection[day.date].append(work_day)


class WorkSchedule:
    def __init__(self, labor, equipment):
        self.labor_days = {}
        self.equipment_days = {}

        for unit in labor:
            add_unit_days(unit, self.labor_days)

        for unit in equipment:
            add_unit_days(unit, self.equipment_days)
