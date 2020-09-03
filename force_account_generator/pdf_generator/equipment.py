from .unit import Unit
from .util import (
    rnd,
    format_date,
    decimal_comma_formatter,
    currency_formatter,
    whole_number_formatter,
    three_decimal_formatter
)
from .paginator import paginate_by_date, simple_paginate
from .page import Page, PageCollection


class Equipment(Unit):
    def __init__(self):
        super().__init__()
        self.description = ''
        self.year = ''
        self.type = ''
        self.configuration = ''
        self.make = ''
        self.model = ''
        self.equipment_number = ''
        self.h_yr = ''
        self.sec_pg = ''
        self.monthly_rate = 0
        self.equipment_adjustment = 0
        self.area_adjustment = 0
        self.operating_cost = 0

    def __repr__(self):
        return 'Equipment(' + self.description + ' - ' + self.equipment_number + ')'

    @property
    def adjusted_hourly_rate(self):
        if self.monthly_rate is None or self.equipment_adjustment is None or self.area_adjustment is None:
            return 0
        rate = (self.monthly_rate * self.equipment_adjustment * self.area_adjustment) / 176
        return rnd(rate)

    @property
    def total_hourly_rate_op(self):
        return (self.adjusted_hourly_rate or 0) + (self.operating_cost or 0)

    @property
    def total_hourly_rate_sb(self):
        return rnd((self.adjusted_hourly_rate or 0) * 0.5)

    @property
    def total_cost_op(self):
        return self.get_total_hours() * (self.total_hourly_rate_op or 0)

    @property
    def total_cost_sb(self):
        return self.get_total_hours(secondary=True) * (self.total_hourly_rate_sb or 0)


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
            self.__set_description(i + 1, unit['description'])
            total_op_hours = 0
            total_sb_hours = 0
            for hours in unit['daily_hours']:
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
        formatted_date = format_date(date, '%m/%d')
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


class EquipmentBreakdownPage(Page):
    def __init__(self, units, field_config, is_first_page):
        template = field_config.template(is_supp=not is_first_page)
        super().__init__(field_config, template)
        self.__units = units
        self.__is_first_page = is_first_page
        self.__hourly_cost_subtotal = 0
        self.__calc_subtotal()
        self.__set_fields()
        self.__fill_blanks()

    def __calc_subtotal(self):
        for unit in self.__units:
            self.__hourly_cost_subtotal += unit.total_cost_op + unit.total_cost_sb

    def __set_fields(self):
        self.__set_subtotal(self.__hourly_cost_subtotal)
        for i, unit in enumerate(self.__units):
            self.__set_description(i + 1, unit.description)
            self.__set_year(i + 1, unit.year)
            self.__set_h_yr(i + 1, unit.h_yr)
            self.__set_sec_pg(i + 1, unit.sec_pg)
            self.__set_monthly_rate(i + 1, unit.monthly_rate)
            self.__set_equipment_adjustment(i + 1, unit.equipment_adjustment)
            self.__set_area_adjustment(i + 1, unit.area_adjustment)
            self.__set_adjusted_hourly_rate(i + 1, unit.adjusted_hourly_rate)
            self.__set_operating_cost(i + 1, unit.operating_cost)
            self.__set_total_hourly_rate_op(i + 1, unit.total_hourly_rate_op)
            self.__set_total_hourly_rate_sb(i + 1, unit.total_hourly_rate_sb)
            self.__set_hours_op(i + 1, unit.get_total_hours())
            self.__set_hours_sb(i + 1, unit.get_total_hours(secondary=True))
            self.__set_amount_op(i + 1, unit.total_cost_op)
            self.__set_amount_sb(i + 1, unit.total_cost_sb)

    def __set_subtotal(self, subtotal):
        field = self._field_config.amount_subtotal(is_supp=not self.__is_first_page)
        self.make_field(field, subtotal, formatter=currency_formatter)

    def __set_description(self, row, description):
        field = self._field_config.description(is_supp=not self.__is_first_page)
        self.make_field(field, description, row=row)

    def __set_year(self, row, year):
        field = self._field_config.year(is_supp=not self.__is_first_page)
        self.make_field(field, year, row=row)

    def __set_h_yr(self, row, h_yr):
        field = self._field_config.h_yr(is_supp=not self.__is_first_page)
        self.make_field(field, h_yr, row=row)

    def __set_sec_pg(self, row, sec_pg):
        field = self._field_config.sec_pg(is_supp=not self.__is_first_page)
        self.make_field(field, sec_pg, row=row)

    def __set_monthly_rate(self, row, monthly_rate):
        if monthly_rate is None:
            return
        field = self._field_config.monthly_rate(is_supp=not self.__is_first_page)
        self.make_field(field, monthly_rate, row=row, formatter=whole_number_formatter)

    def __set_equipment_adjustment(self, row, equipment_adjustment):
        if equipment_adjustment is None:
            return
        field = self._field_config.equipment_adjustment(is_supp=not self.__is_first_page)
        self.make_field(field, equipment_adjustment, row=row, formatter=three_decimal_formatter)

    def __set_area_adjustment(self, row, area_adjustment):
        if area_adjustment is None:
            return
        field = self._field_config.area_adjustment(is_supp=not self.__is_first_page)
        self.make_field(field, area_adjustment, row=row, formatter=three_decimal_formatter)

    def __set_adjusted_hourly_rate(self, row, rate):
        if rate is None:
            return
        field = self._field_config.adjusted_hourly_rate(is_supp=not self.__is_first_page)
        self.make_field(field, rate, row=row, formatter=decimal_comma_formatter)

    def __set_operating_cost(self, row, operating_cost):
        if operating_cost is None:
            return
        field = self._field_config.operating_cost(is_supp=not self.__is_first_page)
        self.make_field(field, operating_cost, row=row, formatter=decimal_comma_formatter)

    def __set_total_hourly_rate_op(self, row, rate):
        if rate is None:
            return
        field = self._field_config.total_hourly_rate_op(is_supp=not self.__is_first_page)
        self.make_field(field, rate, row=row, formatter=decimal_comma_formatter)

    def __set_total_hourly_rate_sb(self, row, rate):
        if rate is None:
            return
        field = self._field_config.total_hourly_rate_sb(is_supp=not self.__is_first_page)
        self.make_field(field, rate, row=row, formatter=decimal_comma_formatter)

    def __set_hours_op(self, row, hours):
        if hours == 0:
            return
        field = self._field_config.hours_op(is_supp=not self.__is_first_page)
        self.make_field(field, hours, row=row, formatter=decimal_comma_formatter)

    def __set_hours_sb(self, row, hours):
        if hours == 0:
            return
        field = self._field_config.hours_sb(is_supp=not self.__is_first_page)
        self.make_field(field, hours, row=row, formatter=decimal_comma_formatter)

    def __set_amount_op(self, row, amount):
        field = self._field_config.amount_op(is_supp=not self.__is_first_page)
        self.make_field(field, amount, row=row, formatter=currency_formatter)

    def __set_amount_sb(self, row, amount):
        field = self._field_config.amount_sb(is_supp=not self.__is_first_page)
        self.make_field(field, amount, row=row, formatter=currency_formatter)

    def __fill_blanks(self):
        self.fill_blanks(
            self._field_config.adjusted_hourly_rate(is_supp=not self.__is_first_page),
            self._field_config.row_count(),
            value=0,
            formatter=decimal_comma_formatter
        )
        self.fill_blanks(
            self._field_config.total_hourly_rate_op(is_supp=not self.__is_first_page),
            self._field_config.row_count(),
            value=0,
            formatter=decimal_comma_formatter
        )
        self.fill_blanks(
            self._field_config.total_hourly_rate_sb(is_supp=not self.__is_first_page),
            self._field_config.row_count(),
            value=0,
            formatter=decimal_comma_formatter
        )
        self.fill_blanks(
            self._field_config.amount_op(is_supp=not self.__is_first_page),
            self._field_config.row_count(),
            value=0,
            formatter=currency_formatter
        )
        self.fill_blanks(
            self._field_config.amount_sb(is_supp=not self.__is_first_page),
            self._field_config.row_count(),
            value=0,
            formatter=currency_formatter
        )


class EquipmentCollection(PageCollection):
    def __init__(self, data_loader, field_config):
        super().__init__(data_loader, field_config)
        self.__equipment = data_loader.equipment
        self.__paginated_daily_equipment = paginate_by_date(
            self.__equipment,
            picked_attrs=['description'],
            date_limit=self._field_config.daily_equipment.column_count(),
            unit_limit=self._field_config.daily_equipment.row_count()
        )
        self.total_cost = 0
        self.__calc_totals()
        self.__create_pages()
        self._populate_headers()

    def __calc_totals(self):
        for unit in self.__equipment:
            self.total_cost += unit.total_cost_op + unit.total_cost_sb

    def __create_pages(self):
        if len(self.__paginated_daily_equipment) == 0:
            return
        self.__create_daily_pages()
        self.__create_breakdown_pages()

    def __create_daily_pages(self):
        daily_pages = []
        for data_set in self.__paginated_daily_equipment:
            for unit_set in data_set['unit_sets']:
                page = DailyEquipmentPage(
                    data_set['dates'],
                    unit_set,
                    self._field_config.daily_equipment
                )
                daily_pages.append(page)
        self.pages += daily_pages

    def __create_breakdown_pages(self):
        breakdown_pages = []
        paginated_equipment = simple_paginate(self.__equipment, self._field_config.equipment_breakdown.row_count())
        for i, equipment_set in enumerate(paginated_equipment):
            breakdown_pages.append(EquipmentBreakdownPage(
                equipment_set,
                self._field_config.equipment_breakdown,
                i == 0))
            if i == 0:
                self.__set_totals(breakdown_pages[0])
        self.pages += breakdown_pages

    def __set_totals(self, page):
        page.make_field(
            self._field_config.equipment_breakdown.amount_total(),
            self.total_cost,
            formatter=currency_formatter
        )
