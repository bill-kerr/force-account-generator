from unit import Unit
from util import rnd, format_date, decimal_comma_formatter
from paginator import paginate_by_date
from page import Page, PageCollection


class Equipment(Unit):
    def __init__(self):
        super().__init__()
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

    def __repr__(self):
        return "Equipment(" + self.description + " - " + self.equipment_number + ")"

    @property
    def adjusted_hourly_rate(self):
        rate = (self.monthly_rate * self.equipment_adjustment * self.area_adjustment) / 176
        return rnd(rate)

    @property
    def total_hourly_rate_op(self):
        return self.adjusted_hourly_rate + self.operating_cost

    @property
    def total_hourly_rate_sb(self):
        return rnd(self.adjusted_hourly_rate * 0.5)

    @property
    def total_cost_op(self):
        return self.get_total_hours() * self.total_hourly_rate_op

    @property
    def total_cost_sb(self):
        return self.get_total_hours(secondary=True) * self.total_hourly_rate_sb


class DailyEquipmentPage(Page):
    def __init__(self, dates, units, field_config):
        super().__init__(field_config, field_config.template())
        self.__dates = dates
        self.__units = units
        self.__set_fields()
        self.__fill_blanks()

    def __set_fields(self):
        for i, date in enumerate(self.__dates):
            self.__set_date(i + 1, date)

        for i, unit in enumerate(self.__units):
            self.__set_description(i + 1, unit["description"])
            total_op_hours = 0
            total_sb_hours = 0
            for hours in unit["daily_hours"]:
                column = self.__dates.index(hours.date) + 1
                total_op_hours += self.__set_op_hours(i + 1, column, hours.primary_hours)
                total_sb_hours += self.__set_sb_hours(i + 1, column, hours.secondary_hours)
            self.__set_total_op(i + 1, total_op_hours)
            self.__set_total_sb(i + 1, total_sb_hours)

    def __fill_blanks(self):
        self.fill_blanks(
            self._field_config.total_op(),
            self._field_config.row_count(),
            value=0,
            formatter=decimal_comma_formatter)
        self.fill_blanks(
            self._field_config.total_sb(),
            self._field_config.row_count(),
            value=0,
            formatter=decimal_comma_formatter
        )

    def __set_date(self, column, date):
        formatted_date = format_date(date, "%m/%d")
        self.make_field(self._field_config.day(), formatted_date, column=column)

    def __set_description(self, row, description):
        field = self._field_config.description()
        self.make_field(field, description, row=row)

    def __set_op_hours(self, row, column, hours):
        if hours is None:
            return 0
        field = self._field_config.hours_op()
        self.make_field(field, hours, row=row, column=column, formatter=decimal_comma_formatter)
        return hours

    def __set_sb_hours(self, row, column, hours):
        if hours is None:
            return 0
        field = self._field_config.hours_sb()
        self.make_field(field, hours, row=row, column=column, formatter=decimal_comma_formatter)
        return hours

    def __set_total_op(self, row, hours):
        field = self._field_config.total_op()
        self.make_field(field, hours, row=row, formatter=decimal_comma_formatter)

    def __set_total_sb(self, row, hours):
        field = self._field_config.total_sb()
        self.make_field(field, hours, row=row, formatter=decimal_comma_formatter)


class EquipmentCollection(PageCollection):
    def __init__(self, input_data, field_config):
        super().__init__(input_data, field_config)
        self.__equipment = input_data.equipment
        self.__paginated_daily_equipment = paginate_by_date(
            self.__equipment,
            picked_attrs=["description"],
            date_limit=self._field_config.daily_equipment.column_count(),
            unit_limit=self._field_config.daily_equipment.row_count()
        )
        self.__create_pages()
        self._populate_headers()

    def __create_pages(self):
        if len(self.__paginated_daily_equipment) == 0:
            return
        self.__create_daily_pages()

    def __create_daily_pages(self):
        daily_pages = []
        for data_set in self.__paginated_daily_equipment:
            for unit_set in data_set["unit_sets"]:
                page = DailyEquipmentPage(
                    data_set["dates"],
                    unit_set,
                    self._field_config.daily_equipment
                )
                daily_pages.append(page)
        self.pages += daily_pages
