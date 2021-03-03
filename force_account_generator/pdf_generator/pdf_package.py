from PyPDF2.generic import NameObject, createStringObject
from .material import MaterialCollection
from .labor import LaborCollection
from .equipment import EquipmentCollection
from .rentals_and_services import RentalsAndServicesCollection
from .consumables import ConsumablesCollection
from .summary import SummaryData, SummaryPage
from .pdf_writer import make_pdf
from .daily import DailyCollection


class PdfPackage:
    def __init__(self, data_loader, pdf_config, daily_sheets=False, callback=None):
        self.__data_loader = data_loader
        self.__pdf_config = pdf_config
        self.__make_daily_sheets = daily_sheets
        self.__callback = callback
        self.__pages = []
        self.__material = MaterialCollection(self.__data_loader, self.__pdf_config)
        self.__labor = LaborCollection(self.__data_loader, self.__pdf_config)
        self.__equipment = EquipmentCollection(self.__data_loader, self.__pdf_config)
        self.__rentals_and_services = RentalsAndServicesCollection(self.__data_loader, self.__pdf_config)
        self.__consumables = ConsumablesCollection(self.__data_loader, self.__pdf_config)
        self.__summary_page = SummaryPage(self.__generate_summary_data(), self.__pdf_config)
        if daily_sheets:
            self.__generate_daily_sheets()

    def __generate_summary_data(self):
        summary_data = SummaryData()
        summary_data.county = self.__data_loader.global_data.county
        summary_data.state_route = self.__data_loader.global_data.state_route
        summary_data.section = self.__data_loader.global_data.section
        summary_data.work_order_number = self.__data_loader.global_data.work_order_number
        summary_data.contract = self.__data_loader.global_data.contract
        summary_data.item_number = self.__data_loader.global_data.item_number
        summary_data.material_cost = self.__material.total_cost
        summary_data.direct_labor_cost = self.__labor.direct_labor_total
        summary_data.indirect_labor_cost = self.__labor.indirect_labor_total
        summary_data.owned_equipment_cost = self.__equipment.total_cost
        summary_data.rented_equipment_cost = self.__rentals_and_services.total_rental_cost
        summary_data.consumables_cost = self.__consumables.total_consumables_cost
        summary_data.services_cost = self.__rentals_and_services.total_services_cost
        summary_data.prime_contractor = self.__data_loader.global_data.prime_contractor
        summary_data.statement_of_cost = self.__data_loader.global_data.statement_of_cost
        return summary_data

    def __generate_daily_sheets(self):
        self.__daily_sheets = DailyCollection(self.__data_loader, self.__pdf_config)

    def generate_pdf(self):
        self.__pages.append(self.__summary_page)
        self.__pages += self.__material.pages
        self.__pages += self.__labor.pages
        self.__pages += self.__equipment.pages
        self.__pages += self.__rentals_and_services.pages
        self.__pages += self.__consumables.pages

        if self.__make_daily_sheets:
            self.__pages += self.__daily_sheets.pages

        return make_pdf(self.__pages, callback=self.__callback)
