""" The config module holds all of the defined field data for writing to the PDF. """
import json
import os


class PdfFieldConfig:
    """ Represents the overall PDF field config. """

    def __init__(self, callback=None):
        self.__cb = callback

        file_path = os.path.join(os.getcwd(), 'pdf_generator', 'pdf_config.json')
        with open(file_path) as config_file:
            self.__config = json.load(config_file)
        self.__callback({'message': 'JSON pdf config loaded.', 'progress': 0})
        self.daily_config = DailyConfig(self.__config["daily"], self.__config["daily_supp"])
        self.material = MaterialConfig(self.__config["material"], self.__config["material_supp"])
        self.final_summary = FinalSummaryConfig(self.__config["final_summary"])
        self.headers = HeadersConfig(self.__config["force_account_headers"])
        self.daily_labor = DailyLaborConfig(self.__config["daily_labor"])
        self.labor_breakdown = LaborBreakdownConfig(
            self.__config["labor_breakdown"], self.__config["labor_breakdown_supp"])
        self.daily_equipment = DailyEquipmentConfig(self.__config["daily_equipment"])
        self.equipment_breakdown = EquipmentBreakdownConfig(
            self.__config["equipment_breakdown"], self.__config["equipment_breakdown_supp"])
        self.rentals_and_services = RentalsAndServicesConfig(
            self.__config["rentals_and_services"], self.__config["rentals_and_services_supp"])
        self.consumables = ConsumablesConfig(self.__config["consumables"])

    def __callback(self, status):
        if self.__cb is not None:
            self.__cb(status)


class FieldConfig:
    """ Base class for a page of field names. """

    def __init__(self, config, supp_config=None):
        self.has_supp = supp_config is not None
        self.config = config
        self.supp_config = supp_config

    def get(self, field_name):
        """ Returns a function that returns the correct field name, given if the page is supplemental. """
        return lambda is_supp=False: self.get_field_name(field_name, is_supp)

    def get_field_name(self, field_name, is_supp):
        """ Returns the field name based on the state of the field config. """
        if not is_supp or not self.has_supp:
            return self.config[field_name]

        return self.supp_config[field_name]


class DailyConfig(FieldConfig):
    """ Field configuration for daily pages. """

    def __init__(self, config, supp_config):
        super().__init__(config, supp_config=supp_config)
        self.template = self.get("template")
        self.description = self.get("description")
        self.date = self.get("date")
        self.ecms_number = self.get("ecms_number")
        self.sr_sec = self.get("sr_sec")
        self.item_number = self.get("item_number")
        self.authorization_number = self.get("authorization_number")
        self.contractor = self.get("contractor")
        self.subcontractor = self.get("subcontractor")
        self.inspector = self.get("inspector")
        self.locations = self.get("locations")
        self.labor_row_count = self.get("labor_row_count")
        self.labor_name = self.get("labor_name")
        self.labor_classification = self.get("labor_classification")
        self.labor_hours_st = self.get("labor_hours_st")
        self.labor_hours_ot = self.get("labor_hours_ot")
        self.equipment_row_count = self.get("equipment_row_count")
        self.equipment_type = self.get("equipment_type")
        self.equipment_configuration = self.get("equipment_configuration")
        self.equipment_year = self.get("equipment_year")
        self.equipment_make = self.get("equipment_make")
        self.equipment_model = self.get("equipment_model")
        self.equipment_hours_op = self.get("equipment_hours_op")
        self.equipment_hours_sb = self.get("equipment_hours_sb")


class FinalSummaryConfig(FieldConfig):
    """ Field config for the Final Summary page. """

    def __init__(self, config):
        super().__init__(config)
        self.template = self.get("template")
        self.contractor = self.get("contractor")
        self.statement_of_cost = self.get("statement_of_cost")
        self.material_total = self.get("material_total")
        self.material_markup = self.get("material_markup")
        self.direct_labor_total = self.get("direct_labor_total")
        self.direct_labor_markup = self.get("direct_labor_markup")
        self.indirect_labor_total = self.get("indirect_labor_total")
        self.owned_equipment_total = self.get("owned_equipment_total")
        self.rented_equipment_total = self.get("rented_equipment_total")
        self.rented_equipment_markup = self.get("rented_equipment_markup")
        self.consumables_total = self.get("consumables_total")
        self.consumables_markup = self.get("consumables_markup")
        self.contractor_cost_total = self.get("contractor_cost_total")
        self.subcontractor_cost_total = self.get("subcontractor_cost_total")
        self.subcontractor_markup = self.get("subcontractor_markup")
        self.service_by_others_total = self.get("service_by_others_total")
        self.service_by_others_markup = self.get("service_by_others_markup")
        self.grand_total = self.get("grand_total")
        self.contractor_representative = self.get("contractor_representative")
        self.department_representative = self.get("department_representative")


class HeadersConfig(FieldConfig):
    """ Field config for the headers on each page. """

    def __init__(self, config):
        super().__init__(config)
        self.county = config["county"]
        self.state_route = config["state_route"]
        self.section = config["section"]
        self.work_order_number = config["work_order_number"]
        self.contract = config["contract"]
        self.item_number = config["item_number"]


class MaterialConfig(FieldConfig):
    """ Field config for the Material page. """

    def __init__(self, config, supp_config):
        super().__init__(config, supp_config=supp_config)
        self.template = self.get("template")
        self.row_count = self.get("row_count")
        self.description = self.get("description")
        self.quantity = self.get("quantity")
        self.unit = self.get("unit")
        self.unit_price = self.get("unit_price")
        self.invoice_number = self.get("invoice_number")
        self.amount = self.get("amount")
        self.subtotal = self.get("subtotal")
        self.sales_tax = self.get("sales_tax")
        self.total = self.get("total")


class DailyLaborConfig(FieldConfig):
    """ Field config for the daily labor page. """

    def __init__(self, config):
        super().__init__(config)
        self.template = self.get("template")
        self.row_count = self.get("row_count")
        self.column_count = self.get("column_count")
        self.day = self.get("day")
        self.hours_st = self.get("hours_st")
        self.hours_ot = self.get("hours_ot")
        self.classification = self.get("classification")
        self.name = self.get("name")
        self.total_st = self.get("total_st")
        self.total_ot = self.get("total_ot")


class LaborBreakdownConfig(FieldConfig):
    """ Field config for the Labor Breakdown page. """

    def __init__(self, config, supp_config):
        super().__init__(config, supp_config=supp_config)
        self.template = self.get("template")
        self.row_count = self.get("row_count")
        self.base_labor_subtotal = self.get("base_labor_subtotal")
        self.social_security_tax_rate = self.get("social_security_tax_rate")
        self.medicare_tax_rate = self.get("medicare_tax_rate")
        self.unemployment_tax_rate = self.get("unemployment_tax_rate")
        self.workers_comp_insurance_rate = self.get("workers_comp_insurance_rate")
        self.liability_insurance_rate = self.get("liability_insurance_rate")
        self.total_taxes_and_insurance = self.get("total_taxes_and_insurance")
        self.direct_labor_subtotal = self.get("direct_labor_subtotal")
        self.indirect_labor_subtotal = self.get("indirect_labor_subtotal")
        self.direct_labor_total = self.get("direct_labor_total")
        self.indirect_labor_total = self.get("indirect_labor_total")
        self.classification = self.get("classification")
        self.name = self.get("name")
        self.hours_st = self.get("hours_st")
        self.hours_ot = self.get("hours_ot")
        self.base_rate_st = self.get("base_rate_st")
        self.base_rate_ot = self.get("base_rate_ot")
        self.hw_pension_rate_st = self.get("hw_pension_rate_st")
        self.hw_pension_rate_ot = self.get("hw_pension_rate_ot")
        self.base_labor_cost_st = self.get("base_labor_cost_st")
        self.base_labor_cost_ot = self.get("base_labor_cost_ot")
        self.direct_labor_rate_st = self.get("direct_labor_rate_st")
        self.direct_labor_rate_ot = self.get("direct_labor_rate_ot")
        self.direct_labor_cost_st = self.get("direct_labor_cost_st")
        self.direct_labor_cost_ot = self.get("direct_labor_cost_ot")


class DailyEquipmentConfig(FieldConfig):
    """ Field config for the Daily Equipment page. """

    def __init__(self, config):
        super().__init__(config)
        self.template = self.get("template")
        self.row_count = self.get("row_count")
        self.column_count = self.get("column_count")
        self.day = self.get("day")
        self.hours_op = self.get("hours_op")
        self.hours_sb = self.get("hours_sb")
        self.description = self.get("description")
        self.total_op = self.get("total_op")
        self.total_sb = self.get("total_sb")


class EquipmentBreakdownConfig(FieldConfig):
    """ Field config for the Equipment Breakdown page. """

    def __init__(self, config, supp_config):
        super().__init__(config, supp_config=supp_config)
        self.template = self.get("template")
        self.row_count = self.get("row_count")
        self.amount_subtotal = self.get("amount_subtotal")
        self.amount_total = self.get("amount_total")
        self.description = self.get("description")
        self.year = self.get("year")
        self.h_yr = self.get("h_yr")
        self.sec_pg = self.get("sec_pg")
        self.monthly_rate = self.get("monthly_rate")
        self.equipment_adjustment = self.get("equipment_adjustment")
        self.area_adjustment = self.get("area_adjustment")
        self.adjusted_hourly_rate = self.get("adjusted_hourly_rate")
        self.operating_cost = self.get("operating_cost")
        self.total_hourly_rate_op = self.get("total_hourly_rate_op")
        self.total_hourly_rate_sb = self.get("total_hourly_rate_sb")
        self.hours_op = self.get("hours_op")
        self.hours_sb = self.get("hours_sb")
        self.amount_op = self.get("amount_op")
        self.amount_sb = self.get("amount_sb")


class RentalsAndServicesConfig(FieldConfig):
    """ Field config for the Rentals and Services page. """

    def __init__(self, config, supp_config):
        super().__init__(config, supp_config=supp_config)
        self.template = self.get("template")
        self.rental_row_count = self.get("rental_row_count")
        self.service_row_count = self.get("service_row_count")
        self.rental_subtotal = self.get("rental_subtotal")
        self.rental_total = self.get("rental_total")
        self.service_subtotal = self.get("service_subtotal")
        self.service_total = self.get("service_total")
        self.rental_description = self.get("rental_description")
        self.rental_invoice_number = self.get("rental_invoice_number")
        self.rental_amount = self.get("rental_amount")
        self.service_description = self.get("service_description")
        self.service_invoice_number = self.get("service_invoice_number")
        self.service_amount = self.get("service_amount")


class ConsumablesConfig(FieldConfig):
    """ Field config for the Consumables page. """

    def __init__(self, config):
        super().__init__(config)
        self.template = self.get("template")
        self.purchased_consumables_row_count = self.get("purchased_consumables_row_count")
        self.stock_consumables_row_count = self.get("stock_consumables_row_count")
        self.consumables_total = self.get("consumables_total")
        self.purchased_consumable_description = self.get("purchased_consumable_description")
        self.purchased_consumable_quantity = self.get("purchased_consumable_quantity")
        self.purchased_consumable_unit_price = self.get("purchased_consumable_unit_price")
        self.purchased_consumable_invoice_number = self.get("purchased_consumable_invoice_number")
        self.purchased_consumable_amount = self.get("purchased_consumable_amount")
        self.purchased_consumable_subtotal = self.get("purchased_consumable_subtotal")
        self.stock_consumable_description = self.get("stock_consumable_description")
        self.stock_consumable_invoice_value = self.get("stock_consumable_invoice_value")
        self.stock_consumable_percent_reimbursed = self.get("stock_consumable_percent_reimbursed")
        self.stock_consumable_invoice_number = self.get("stock_consumable_invoice_number")
        self.stock_consumable_amount = self.get("stock_consumable_amount")
        self.stock_consumable_subtotal = self.get("stock_consumable_subtotal")
