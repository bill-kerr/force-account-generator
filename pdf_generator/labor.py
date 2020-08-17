""" The labor file includes the Labor model and requisite page classes for constructing the labor
portion of a force account. """
from hours import Hours
from util import make_field
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
        hours = Hours(date, straight_time, overtime)
        self.daily_hours[date] = hours


class DailyLaborPage:
    def __init__(self, dates, field_config):
        self.__dates = dates
        self.__field_config = field_config
        self.values = {}
        self.__st_hours = {}
        self.__ot_hours = {}
        self.__set_fields()
        print(self.values)

    def __set_fields(self):
        for i, date in enumerate(self.__dates):
            for j, labor_unit in enumerate(date["units"]):
                if i == 0:
                    self.__set_classification(j, labor_unit["classification"])
                    self.__set_name(j, labor_unit["name"])
  
                self.__add_hours(labor_unit)
                self.__set_st_hours(j, i, labor_unit["primary_hours"])
                self.__set_ot_hours(j, i, labor_unit["secondary_hours"])

    def __make_field(self, field, row, value):
        if not value:
            return
        value = str(value)
        make_field(self.values, field, row + 1, value)

    def __add_hours(self, labor_unit, st_hours_label="primary_hours", ot_hours_label="secondary_hours"):
        if labor_unit["id"] not in self.__st_hours and labor_unit[st_hours_label] is not None:
            self.__st_hours[labor_unit["id"]] = labor_unit[st_hours_label]
        elif labor_unit[st_hours_label] is not None:
            self.__st_hours[labor_unit["id"]] += labor_unit[st_hours_label]

        if labor_unit["id"] not in self.__ot_hours and labor_unit[ot_hours_label] is not None:
            self.__ot_hours[labor_unit["id"]] = labor_unit[ot_hours_label]
        elif labor_unit[ot_hours_label] is not None:
            self.__ot_hours[labor_unit["id"]] += labor_unit[ot_hours_label]


    def __set_classification(self, row, value):
        field = self.__field_config.classification()
        self.__make_field(field, row, value)

    def __set_name(self, row, value):
        field = self.__field_config.name()
        self.__make_field(field, row, value)

    def __set_st_hours(self, row, column, value):
        if value is None:
            return
        field = self.__field_config.hours_st() + "_" + str(row)
        self.__make_field(field, column, f'{value:,.2f}')

    def __set_ot_hours(self, row, column, value):
        if value is None:
            return
        field = self.__field_config.hours_ot() + "_" + str(row)
        self.__make_field(field, column, f'{value:,.2f}')


class DailyLaborCollection:
    """ DailyLaborCollection represents multiple daily labor pages. """
    def __init__(self, date_set, field_config):
        self.__date_set = date_set
        self.__field_config = field_config
        self.__pages = []
        self.__create_pages()

    def __create_pages(self):
        for date in self.__date_set:
            for labor_set in date["units"]:
                # self.__pages.append(DailyLaborPage())
                pass

    def get_pages(self):
        return self.__pages


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
        for date_set in self.__paginated_daily_labor:
            daily_pages.append(DailyLaborCollection(date_set, self.__field_config).get_pages())

        self.__pages.append(daily_pages)
