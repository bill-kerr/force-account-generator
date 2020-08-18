""" The labor file includes the Labor model and requisite page classes for constructing the labor
portion of a force account. """
from hours import Hours
from util import format_date, rnd, decimal_comma_formatter, currency_formatter
from paginator import paginate_by_date, simple_paginate
from page import Page


class Labor:
    """ The Labor class represents a single labor resource. """

    def __init__(self):
        self.classification = ""
        self.name = ""
        self.base_rate_st = 0
        self.base_rate_ot = 0
        self.hw_pension_rate_st = 0
        self.hw_pension_rate_ot = 0
        self.daily_hours = {}

    def __repr__(self):
        return "Labor(" + self.classification + " - " + self.name + ")"

    def add_daily_hours(self, date, straight_time, overtime):
        """ Adds a set of straight time and overtime hours to the Labor object. """
        hours = Hours(date, straight_time, overtime)
        self.daily_hours[date] = hours

    def get_total_hours(self, secondary=False):
        total_hours = 0
        for hours in self.daily_hours.values():
            total_hours += (hours.primary_hours or 0) if not secondary else (hours.secondary_hours or 0)
        return total_hours

    @property
    def base_labor_cost_st(self):
        total_hours = self.get_total_hours()
        return rnd(total_hours * self.base_rate_st)

    @property
    def base_labor_cost_ot(self):
        total_hours = self.get_total_hours(secondary=True)
        return rnd(total_hours * self.base_rate_st)

    @property
    def direct_labor_rate_st(self):
        return rnd(self.base_rate_st + self.hw_pension_rate_st)

    @property
    def direct_labor_rate_ot(self):
        return rnd(self.base_rate_ot + self.hw_pension_rate_ot)

    @property
    def direct_labor_cost_st(self):
        return rnd(self.direct_labor_rate_st * self.get_total_hours())

    @property
    def direct_labor_cost_ot(self):
        return rnd(self.direct_labor_rate_ot * self.get_total_hours(secondary=True))


class DailyLaborPage(Page):
    """ DailyLaborPage represents a single daily labor page. """

    def __init__(self, dates, units, field_config):
        super().__init__(field_config)
        self.__dates = dates
        self.__units = units
        self.__set_fields()

    def __set_fields(self):
        for i, date in enumerate(self.__dates):
            self.__set_date(i + 1, date)

        for i, unit in enumerate(self.__units):
            self.__set_classification(i, unit["classification"])
            self.__set_name(i, unit["name"])
            total_st_hours = 0
            total_ot_hours = 0
            for hours in unit["daily_hours"]:
                column = self.__dates.index(hours.date)
                total_st_hours += self.__set_st_hours(
                    i, column, hours.primary_hours)
                total_ot_hours += self.__set_ot_hours(
                    i, column, hours.secondary_hours)
            self.__set_total_st(i, total_st_hours)
            self.__set_total_ot(i, total_ot_hours)

    def __set_date(self, column, date):
        formatted_date = format_date(date, "%m/%d")
        self._make_field(self._field_config.day(), formatted_date, column=column)

    def __set_classification(self, row, classification):
        field = self._field_config.classification()
        self._make_field(field, classification, row=row)

    def __set_name(self, row, name):
        field = self._field_config.name()
        self._make_field(field, name, row=row)

    def __set_st_hours(self, row, column, hours):
        if hours is None:
            return 0
        field = self._field_config.hours_st()
        self._make_field(field, hours, row=row, column=column, formatter=decimal_comma_formatter)
        return hours

    def __set_ot_hours(self, row, column, hours):
        if hours is None:
            return 0
        field = self._field_config.hours_ot()
        self._make_field(field, hours, row=row, column=column, formatter=decimal_comma_formatter)
        return hours

    def __set_total_st(self, row, hours):
        field = self._field_config.total_st()
        self._make_field(field, hours, row=row, formatter=decimal_comma_formatter)

    def __set_total_ot(self, row, hours):
        field = self._field_config.total_ot()
        self._make_field(field, hours, row=row, formatter=decimal_comma_formatter)


class LaborBreakdownPage(Page):
    def __init__(self, units, field_config, taxes_and_insurance, is_first_page):
        super().__init__(field_config)
        self.__units = units
        self.__taxes_and_insurance = taxes_and_insurance
        self.__is_first_page = is_first_page
        self.__base_labor_subtotal = 0
        self.__direct_labor_subtotal = 0
        self.__indirect_labor_subtotal = 0
        self.__calc_subtotals()
        self.__set_fields()

    def __calc_subtotals(self):
        for unit in self.__units:
            self.__base_labor_subtotal += unit.base_labor_cost_st + unit.base_labor_cost_ot
            self.__direct_labor_subtotal += unit.direct_labor_cost_st + unit.direct_labor_cost_ot
        taxes = self.__taxes_and_insurance.total_taxes_and_insurance
        self.__indirect_labor_subtotal = rnd(self.__base_labor_subtotal * taxes)

    def __set_fields(self):
        self.__set_taxes_and_insurance_fields()
        for i, unit in enumerate(self.__units):
            self.__set_classification(i + 1, unit.classification)
            self.__set_name(i + 1, unit.name)
            self.__set_st_hours(i + 1, unit.get_total_hours())
            self.__set_ot_hours(i + 1, unit.get_total_hours(secondary=True))
            self.__set_base_rate_st(i + 1, unit.base_rate_st)
            self.__set_base_rate_ot(i + 1, unit.base_rate_ot)
            self.__set_base_labor_cost_st(i + 1, unit.base_labor_cost_st)
            self.__set_base_labor_cost_ot(i + 1, unit.base_labor_cost_ot)
            self.__set_direct_labor_rate_st(i + 1, unit.direct_labor_rate_st)
            self.__set_direct_labor_rate_ot(i + 1, unit.direct_labor_rate_ot)
            self.__set_direct_labor_cost_st(i + 1, unit.direct_labor_cost_st)
            self.__set_direct_labor_cost_ot(i + 1, unit.direct_labor_cost_ot)

    def __set_taxes_and_insurance_fields(self):
        self.__set_social_security(self.__taxes_and_insurance.social_security)
        self.__set_medicare(self.__taxes_and_insurance.medicare)
        self.__set_unemployment(self.__taxes_and_insurance.unemployment)
        self.__set_workers_comp(self.__taxes_and_insurance.workers_comp)
        self.__set_liability(self.__taxes_and_insurance.liability)
        self.__set_total_taxes_and_insurance(self.__taxes_and_insurance.total_taxes_and_insurance)

    def __set_social_security(self, rate):
        field = self._field_config.social_security_tax_rate(is_supp=not self.__is_first_page)
        self._make_field(field, rate)

    def __set_medicare(self, rate):
        field = self._field_config.medicare_tax_rate(is_supp=not self.__is_first_page)
        self._make_field(field, rate)

    def __set_unemployment(self, rate):
        field = self._field_config.unemployment_tax_rate(is_supp=not self.__is_first_page)
        self._make_field(field, rate)

    def __set_workers_comp(self, rate):
        field = self._field_config.workers_comp_insurance_rate(is_supp=not self.__is_first_page)
        self._make_field(field, rate)

    def __set_liability(self, rate):
        field = self._field_config.liability_insurance_rate(is_supp=not self.__is_first_page)
        self._make_field(field, rate)

    def __set_total_taxes_and_insurance(self, rate):
        field = self._field_config.total_taxes_and_insurance(is_supp=not self.__is_first_page)
        self._make_field(field, rate)

    def __set_classification(self, row, classification):
        field = self._field_config.classification(is_supp=not self.__is_first_page)
        self._make_field(field, classification, row=row)

    def __set_name(self, row, name):
        field = self._field_config.name(is_supp=not self.__is_first_page)
        self._make_field(field, name, row=row)

    def __set_st_hours(self, row, hours):
        field = self._field_config.hours_st(is_supp=not self.__is_first_page)
        self._make_field(field, hours, row=row, formatter=decimal_comma_formatter)

    def __set_ot_hours(self, row, hours):
        field = self._field_config.hours_ot(is_supp=not self.__is_first_page)
        self._make_field(field, hours, row=row, formatter=decimal_comma_formatter)

    def __set_base_rate_st(self, row, rate):
        field = self._field_config.base_rate_st(is_supp=not self.__is_first_page)
        self._make_field(field, rate, row=row, formatter=decimal_comma_formatter)

    def __set_base_rate_ot(self, row, rate):
        field = self._field_config.base_rate_ot(is_supp=not self.__is_first_page)
        self._make_field(field, rate, row=row, formatter=decimal_comma_formatter)

    def __set_base_labor_cost_st(self, row, cost):
        field = self._field_config.base_labor_cost_st(is_supp=not self.__is_first_page)
        self._make_field(field, cost, row=row, formatter=currency_formatter)

    def __set_base_labor_cost_ot(self, row, cost):
        field = self._field_config.base_labor_cost_ot(is_supp=not self.__is_first_page)
        self._make_field(field, cost, row=row, formatter=currency_formatter)

    def __set_direct_labor_rate_st(self, row, rate):
        field = self._field_config.direct_labor_rate_st(is_supp=not self.__is_first_page)
        self._make_field(field, rate, row=row, formatter=decimal_comma_formatter)

    def __set_direct_labor_rate_ot(self, row, rate):
        field = self._field_config.direct_labor_rate_ot(is_supp=not self.__is_first_page)
        self._make_field(field, rate, row=row, formatter=decimal_comma_formatter)

    def __set_direct_labor_cost_st(self, row, cost):
        field = self._field_config.direct_labor_cost_st(is_supp=not self.__is_first_page)
        self._make_field(field, cost, row=row, formatter=currency_formatter)

    def __set_direct_labor_cost_ot(self, row, cost):
        field = self._field_config.direct_labor_cost_ot(is_supp=not self.__is_first_page)
        self._make_field(field, cost, row=row, formatter=currency_formatter)


class LaborCollection:
    """ LaborCollection represents all of the labor pages in the current force account. """

    def __init__(self, field_config, input_data):
        self.__labor = input_data.labor
        self.__global_data = input_data.global_data
        self.__field_config = field_config
        self.__paginated_daily_labor = paginate_by_date(
            self.__labor,
            picked_attrs=["classification", "name"],
            date_limit=self.__field_config.daily_labor.column_count(),
            unit_limit=self.__field_config.daily_labor.row_count())
        self.__pages = []
        self.__taxes_and_insurance = TaxesAndInsurance(
            self.__global_data.social_security_tax_rate,
            self.__global_data.medicare_tax_rate,
            self.__global_data.unemployment_tax_rate,
            self.__global_data.workers_comp_insurance_rate,
            self.__global_data.liability_insurance_rate
        )
        self.__create_pages()

    def __create_pages(self):
        if len(self.__paginated_daily_labor) == 0:
            return

        daily_pages = []
        for data_set in self.__paginated_daily_labor:
            for unit_set in data_set["unit_sets"]:
                page = DailyLaborPage(
                    data_set["dates"], unit_set, self.__field_config.daily_labor)
                daily_pages.append(page)

        self.__pages.append(daily_pages)

        labor_breakdown_pages = []
        paginated_labor = simple_paginate(self.__labor, self.__field_config.labor_breakdown.row_count())
        for i, labor_set in enumerate(paginated_labor):
            labor_breakdown_pages.append(LaborBreakdownPage(
                labor_set,
                self.__field_config.labor_breakdown,
                self.__taxes_and_insurance,
                i == 0))


class TaxesAndInsurance:
    def __init__(self, social_security, medicare, unemployment, workers_comp, liability):
        self.social_security = social_security
        self.medicare = medicare
        self.unemployment = unemployment
        self.workers_comp = workers_comp
        self.liability = liability
        self.total_taxes_and_insurance = self.__calc_total_taxes_and_insurance()

    def __calc_total_taxes_and_insurance(self):
        return self.social_security + self.medicare + self.unemployment + self.workers_comp + self.liability