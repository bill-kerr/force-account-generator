from itertools import zip_longest
from page import PageCollection, Page
from paginator import simple_paginate
from util import decimal_comma_formatter


class DailyPage(Page):
    def __init__(self, labor, equipment, field_config, is_supp=False):
        super().__init__(field_config, field_config.template(is_supp=is_supp))
        self.__labor = labor
        self.__equipment = equipment
        self.__set_fields()

    def __set_fields(self):
        self.__set_labor_fields()
        self.__set_equipment_fields()

    def __set_labor_fields(self):
        if self.__labor is None:
            return
        for i, unit in enumerate(self.__labor):
            self.make_field(self._field_config.labor_name(), unit["name"], row=i + 1)
            self.make_field(self._field_config.labor_classification(), unit["classification"], row=i + 1)
            self.make_field(
                self._field_config.labor_hours_st(),
                unit["st"],
                formatter=decimal_comma_formatter,
                row=i + 1)
            self.make_field(
                self._field_config.labor_hours_ot(),
                unit["ot"],
                formatter=decimal_comma_formatter,
                row=i + 1)

    def __set_equipment_fields(self):
        if self.__equipment is None:
            return
        for i, unit in enumerate(self.__equipment):
            self.make_field(self._field_config.equipment_type(), unit["type"], row=i + 1)
            self.make_field(self._field_config.equipment_configuration(), unit["configuration"], row=i + 1)
            self.make_field(self._field_config.equipment_year(), unit["year"], row=i + 1)
            self.make_field(self._field_config.equipment_make(), unit["make"], row=i + 1)
            self.make_field(self._field_config.equipment_model(), unit["model"], row=i + 1)
            self.make_field(
                self._field_config.equipment_hours_op(),
                unit["op"],
                row=i + 1,
                formatter=decimal_comma_formatter)
            self.make_field(
                self._field_config.equipment_hours_sb(),
                unit["sb"],
                row=i + 1,
                formatter=decimal_comma_formatter)


class DailyCollection(PageCollection):
    def __init__(self, data_loader, field_config):
        super().__init__(data_loader, field_config.daily_config)
        self.__labor = data_loader.labor
        self.__equipment = data_loader.equipment
        self.__group_by_date()
        self.__create_pages()

    def __group_by_date(self):
        self.__dates = {}
        self.__group_labor_by_date()
        self.__group_equipment_by_date()
        self.__paginate_dates()

    def __group_labor_by_date(self):
        for unit in self.__labor:
            for hours in unit.daily_hours.values():
                if hours.date not in self.__dates:
                    self.__dates[hours.date] = {"labor": [], "equipment": []}
                self.__dates[hours.date]["labor"].append(
                    reduce_labor_unit(unit, st=hours.primary_hours, ot=hours.secondary_hours))

    def __group_equipment_by_date(self):
        for unit in self.__equipment:
            for hours in unit.daily_hours.values():
                if hours.date not in self.__dates:
                    self.__dates[hours.date] = {"labor": [], "equipment": []}
                self.__dates[hours.date]["equipment"].append(
                    reduce_equipment_unit(unit, op=hours.primary_hours, sb=hours.secondary_hours))

    def __paginate_dates(self):
        for date in self.__dates.values():
            date["labor"] = simple_paginate(date["labor"], self._field_config.labor_row_count())
            date["equipment"] = simple_paginate(date["equipment"], self._field_config.equipment_row_count())

    def __create_pages(self):
        for date, units in self.__dates.items():
            zipped_sets = zip_longest(units["labor"], units["equipment"])
            for labor_set, equipment_set in zipped_sets:
                page = DailyPage(labor_set, equipment_set, self._field_config)
                self.__set_headers(page, date)
                self.pages.append(page)
            back_page = DailyPage(None, None, self._field_config, is_supp=True)
            self.__set_headers(back_page, date, is_supp=True)
            self.pages.append(back_page)

    def __set_headers(self, page, date, is_supp=False):
        page.make_field(self._field_config.date(is_supp=is_supp), date)
        page.make_field(self._field_config.ecms_number(is_supp=is_supp), self._global_data.contract)
        sr_sec = self._global_data.state_route + "/" + self._global_data.section
        page.make_field(self._field_config.sr_sec(is_supp=is_supp), sr_sec)
        page.make_field(self._field_config.item_number(is_supp=is_supp), self._global_data.item_number)
        page.make_field(self._field_config.contractor(is_supp=is_supp), self._global_data.prime_contractor)


def reduce_labor_unit(unit, st=0, ot=0):
    reduced_unit = {}
    reduced_unit["name"] = unit.name
    reduced_unit["classification"] = unit.classification
    reduced_unit["st"] = st
    reduced_unit["ot"] = ot
    return reduced_unit


def reduce_equipment_unit(unit, op=0, sb=0):
    reduced_unit = {}
    reduced_unit["type"] = unit.type
    reduced_unit["configuration"] = unit.configuration
    reduced_unit["year"] = unit.year
    reduced_unit["make"] = unit.make
    reduced_unit["model"] = unit.model
    reduced_unit["op"] = op
    reduced_unit["sb"] = sb
    return reduced_unit
