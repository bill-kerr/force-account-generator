""" The labor file includes the Labor model and requisite page classes for constructing the labor
portion of a force account. """
from hours import Hours
from util import make_field, format_date
from paginator import paginate_by_date


class Labor:
    """ The Labor class represents a single labor resource. """
    def __init__(self):
        self.classification = ""
        self.name = ""
        self.base_rate = 0
        self.hw_pension_rate = 0
        self.daily_hours = {}

    def __repr__(self):
        return "Labor(" + self.name + ")"

    def add_daily_hours(self, date, straight_time, overtime):
        """ Adds a set of straight time and overtime hours to the Labor object. """
        hours = Hours(date, straight_time, overtime)
        self.daily_hours[date] = hours


class DailyLaborPage:
    """ DailyLaborPage represents a single daily labor page. """
    def __init__(self, dates, units, field_config):
        self.__dates = dates
        self.__units = units
        self.__field_config = field_config
        self.values = {}
        self.__set_fields()
        print(self.values)

    def __set_fields(self):
        for i, date in enumerate(self.__dates):
            self.__set_date(i, date)

        for i, unit in enumerate(self.__units):
            self.__set_classification(i, unit["classification"])
            self.__set_name(i, unit["name"])
            total_st_hours = 0
            total_ot_hours = 0
            for hours in unit["daily_hours"]:
                column = self.__dates.index(hours.date)
                total_st_hours += self.__set_st_hours(i, column, hours.primary_hours)
                total_ot_hours += self.__set_ot_hours(i, column, hours.secondary_hours)
            self.__set_total_st(i, total_st_hours)
            self.__set_total_ot(i, total_ot_hours)

    def __make_field(self, field, row, value):
        if not value:
            return
        value = str(value)
        make_field(self.values, field, row + 1, value)

    def __set_date(self, column, date):
        formatted_date = format_date(date, "%m/%d")
        make_field(self.values, self.__field_config.day(), column, formatted_date)

    def __set_classification(self, row, classification):
        if classification is None:
            return
        field = self.__field_config.classification()
        self.__make_field(field, row, classification)

    def __set_name(self, row, name):
        if name is None:
            return
        field = self.__field_config.name()
        self.__make_field(field, row, name)

    def __set_st_hours(self, row, column, hours):
        if hours is None:
            return 0
        prefix = "_0" + str(row + 1) if row + 1 < 10 else "_" + str(row + 1)
        field = self.__field_config.hours_st() + prefix
        self.__make_field(field, column, f'{hours:,.2f}')
        return hours

    def __set_ot_hours(self, row, column, hours):
        if hours is None:
            return 0
        prefix = "_0" + str(row + 1) if row + 1 < 10 else "_" + str(row + 1)
        field = self.__field_config.hours_ot() + prefix
        self.__make_field(field, column, f'{hours:,.2f}')
        return hours

    def __set_total_st(self, row, hours):
        field = self.__field_config.total_st()
        self.__make_field(field, row, f'{hours:,.2f}')

    def __set_total_ot(self, row, hours):
        field = self.__field_config.total_ot()
        self.__make_field(field, row, f'{hours:,.2f}')


class LaborCollection:
    """ LaborCollection represents all of the labor pages in the current force account. """
    def __init__(self, field_config, input_data):
        self.__labor = input_data.labor
        self.__global_data = input_data.global_data
        self.__field_config = field_config
        self.__paginated_daily_labor = paginate_by_date(self.__labor, picked_attrs=["classification", "name"])
        self.__pages = []
        self.__create_pages()

    def __create_pages(self):
        if len(self.__paginated_daily_labor) == 0:
            return

        daily_pages = []
        for data_set in self.__paginated_daily_labor:
            for unit_set in data_set["unit_sets"]:
                page = DailyLaborPage(data_set["dates"], unit_set, self.__field_config.daily_labor)
                daily_pages.append(page)

        self.__pages.append(daily_pages)
