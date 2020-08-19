from itertools import zip_longest
from page import PageCollection, Page
from paginator import simple_paginate


class DailyPage(Page):
    def __init__(self, labor, equipment):
        pass


class DailyCollection(PageCollection):
    def __init__(self, data_loader, field_config):
        super().__init__(data_loader, field_config)
        self.__labor_days = group_labor_by_date(data_loader.labor)
        self.__equipment_days = group_equipment_by_date(data_loader.equipment)
        self.__create_pages()

    def __create_pages(self):
        pass


def group_labor_by_date(units):
    dates = {}
    for unit in units:
        for hours in unit.daily_hours.values():
            if hours.date not in dates:
                dates[hours.date] = []
            dates[hours.date].append(reduce_labor_unit(unit, st=hours.primary_hours, ot=hours.secondary_hours))
    return dates


def group_equipment_by_date(units):
    dates = {}
    for unit in units:
        for hours in unit.daily_hours.values():
            if hours.date not in dates:
                dates[hours.date] = []
            dates[hours.date].append(reduce_equipment_unit(unit, op=hours.primary_hours, sb=hours.secondary_hours))
    return dates


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
