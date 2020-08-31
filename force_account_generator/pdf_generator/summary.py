from .page import Page
from .util import rnd, currency_formatter


class SummaryData():
    def __init__(self):
        self.county = ''
        self.state_route = ''
        self.section = ''
        self.work_order_number = ''
        self.contract = ''
        self.item_number = ''
        self.material_cost = 0
        self.direct_labor_cost = 0
        self.indirect_labor_cost = 0
        self.owned_equipment_cost = 0
        self.rented_equipment_cost = 0
        self.consumables_cost = 0
        self.subcontractor_cost = 0
        self.services_cost = 0
        self.prime_contractor = ''
        self.statement_of_cost = ''

    @property
    def material_markup(self):
        return rnd(self.material_cost * 0.15)

    @property
    def direct_labor_markup(self):
        return rnd(self.direct_labor_cost * 0.3)

    @property
    def rental_markup(self):
        return rnd(self.rented_equipment_cost * 0.05)

    @property
    def consumables_markup(self):
        return rnd(self.consumables_cost * 0.05)

    @property
    def contractor_cost_total(self):
        return sum([
            self.material_cost,
            self.material_markup,
            self.direct_labor_cost,
            self.direct_labor_markup,
            self.indirect_labor_cost,
            self.owned_equipment_cost,
            self.rented_equipment_cost,
            self.rental_markup,
            self.consumables_cost,
            self.consumables_markup])

    @property
    def subcontractor_markup(self):
        return rnd(self.subcontractor_cost * 0.05)

    @property
    def services_markup(self):
        return rnd(self.services_cost * 0.05)

    @property
    def grand_total(self):
        return sum([
            self.material_cost,
            self.material_markup,
            self.direct_labor_cost,
            self.direct_labor_markup,
            self.indirect_labor_cost,
            self.owned_equipment_cost,
            self.rented_equipment_cost,
            self.rental_markup,
            self.consumables_cost,
            self.consumables_markup,
            self.subcontractor_cost,
            self.subcontractor_markup,
            self.services_cost,
            self.services_markup])


class SummaryPage(Page):
    def __init__(self, summary_data, pdf_config):
        super().__init__(pdf_config.final_summary, pdf_config.final_summary.template())
        self.__headers_config = pdf_config.headers
        self.__data = summary_data
        self.__set_fields()

    def __set_fields(self):
        self.make_field(self.__headers_config.county, self.__data.county)
        self.make_field(self.__headers_config.state_route, self.__data.state_route)
        self.make_field(self.__headers_config.section, self.__data.section)
        self.make_field(self.__headers_config.work_order_number, self.__data.work_order_number)
        self.make_field(self.__headers_config.contract, self.__data.contract)
        self.make_field(self.__headers_config.item_number, self.__data.item_number)
        self.make_field(self._field_config.contractor(), self.__data.prime_contractor)
        self.make_field(self._field_config.statement_of_cost(), self.__data.statement_of_cost)
        self.__total_field(self._field_config.material_total(), self.__data.material_cost)
        self.__total_field(self._field_config.material_markup(), self.__data.material_markup)
        self.__total_field(self._field_config.direct_labor_total(), self.__data.direct_labor_cost)
        self.__total_field(self._field_config.direct_labor_markup(), self.__data.direct_labor_markup)
        self.__total_field(self._field_config.indirect_labor_total(), self.__data.indirect_labor_cost)
        self.__total_field(self._field_config.owned_equipment_total(), self.__data.owned_equipment_cost)
        self.__total_field(self._field_config.rented_equipment_total(), self.__data.rented_equipment_cost)
        self.__total_field(self._field_config.rented_equipment_markup(), self.__data.rental_markup)
        self.__total_field(self._field_config.consumables_total(), self.__data.consumables_cost)
        self.__total_field(self._field_config.consumables_markup(), self.__data.consumables_markup)
        self.__total_field(self._field_config.contractor_cost_total(), self.__data.contractor_cost_total)
        self.__total_field(self._field_config.subcontractor_cost_total(), self.__data.subcontractor_cost)
        self.__total_field(self._field_config.subcontractor_markup(), self.__data.subcontractor_markup)
        self.__total_field(self._field_config.service_by_others_total(), self.__data.services_cost)
        self.__total_field(self._field_config.service_by_others_markup(), self.__data.services_markup)
        self.__total_field(self._field_config.grand_total(), self.__data.grand_total)

    def __total_field(self, field_name, value):
        self.make_field(field_name, value, formatter=currency_formatter)
