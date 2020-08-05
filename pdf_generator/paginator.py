from work_day import WorkDay


class Paginator:
    def __init__(self, field_config):
        self.__field_config = field_config

    def paginate_by_date(self, units):
        dates = {}
        for unit in units:
            for hours in unit.daily_hours.values():
                if dates.get(hours.date) is None:
                    work_day = WorkDay(hours.date)
                    work_day.units.append(unit)
                    dates[work_day.date] = work_day
                else:
                    dates[hours.date].units.append(unit)
        return dates
