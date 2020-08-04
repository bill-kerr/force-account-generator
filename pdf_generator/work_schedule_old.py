from work_day import WorkDay


class WorkSchedule:
    def __init__(self):
        self.__days = {}

    def __repr__(self):
        days = ''
        for i, day in enumerate(self.__days):
            end = ' ' if i != len(self.__days) - 1 else ''
            days += repr(day) + end
        return 'WorkSchedule(' + days + ')'

    def add_day(self, date):
        if self.__days.get(date) is None:
            self.__days[date] = WorkDay(date)
        return self.__days[date]

    def get_day(self, date):
        return self.__days.get(date)

    def get_days(self, start_date=None, end_date=None):
        if start_date is None and end_date is None:
            return self.__days

        days = []
        for day in self.__days:
            if end_date is not None and start_date is None and day <= end_date:
                days.append(day)
            elif start_date is not None and end_date is None and day >= start_date:
                days.append(day)
            elif end_date is not None and start_date is not None and start_date <= day <= end_date:
                days.append(day)
        return days
