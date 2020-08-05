import json


class DailyConfig:
    def __init__(self, config, supp_config):
        self.template = config["template"]
        self.description = config["description"]
        self.date = config["headers"]["date"]
        self.ecms_number = config["headers"]["ecms_number"]
        self.sr_sec = config["headers"]["sr_sec"]
        self.item_number = config["headers"]["item_number"]
        self.authorization_number = config["headers"]["authorization_number"]
        self.contractor = config["headers"]["contractor"]
        self.subcontractor = config["headers"]["subcontractor"]
        self.inspector = config["headers"]["inspector"]
        self.locations = config["headers"]["locations"]
        self.labor_row_count = config["labor"]["row_count"]
        self.labor_name = config["labor"]["fields"]["name"]
        self.labor_classification = config["labor"]["fields"]["classification"]
        self.labor_hours_st = config["labor"]["fields"]["hours_st"]
        self.labor_hours_ot = config["labor"]["fields"]["hours_ot"]
        self.equipment_row_count = config["equipment"]["row_count"]
        self.equipment_type = config["equipment"]["fields"]["equipment_type"]
        self.equipment_configuration = config["equipment"]["fields"]["configuration"]
        self.equipment_year = config["equipment"]["fields"]["year"]
        self.equipment_make = config["equipment"]["fields"]["make"]
        self.equipment_model = config["equipment"]["fields"]["model"]
        self.equipment_hours_op = config["equipment"]["fields"]["hours_op"]
        self.equipment_hours_sb = config["equipment"]["fields"]["hours_sb"]
        self.template_supp = supp_config["template"]
        self.date_supp = supp_config["headers"]["date"]
        self.ecms_number_supp = supp_config["headers"]["ecms_number"]
        self.sr_sec_supp = supp_config["headers"]["sr_sec"]
        self.item_number_supp = supp_config["headers"]["item_number"]
        self.authorization_number_supp = supp_config["headers"]["authorization_number"]
        self.contractor_supp = supp_config["headers"]["contractor"]
        self.subcontractor_supp = supp_config["headers"]["subcontractor"]
        self.inspector_supp = supp_config["headers"]["inspector"]
        self.locations_supp = supp_config["headers"]["locations"]


class FinalSummaryConfig:
    def __init__(self, config):
        self.template = config["template"]
        self.contractor = config["contractor"]
        self.statement_of_cost = config["statement_of_cost"]
        self.material_total = config["material_total"]
        self.material_markup = config["material_markup"]
        self.direct_labor_total = config["direct_labor_total"]
        self.direct_labor_markup = config["direct_labor_markup"]
        self.indirect_labor_total = config["indirect_labor_total"]
        self.owned_equipment_total = config["owned_equipment_total"]
        self.rented_equipment_total = config["rented_equipment_total"]
        self.consumables_total = config["consumables_total"]
        self.consumables_markup = config["consumables_markup"]
        self.contractor_cost_total = config["contractor_cost_total"]
        self.subcontractor_cost_total = config["subcontractor_cost_total"]
        self.service_by_others_total = config["service_by_others_total"]
        self.service_by_others_markup = config["service_by_others_markup"]
        self.grand_total = config["grand_total"]
        self.contractor_representative = config["contractor_representative"]
        self.department_representative = config["department_representative"]


class HeadersConfig:
    def __init__(self, config):
        self.county = config["county"]
        self.state_route = config["state_route"]
        self.section = config["section"]
        self.work_order_number = config["work_order_number"]
        self.contract = config["contract"]
        self.item_number = config["item_number"]


class MaterialConfig:
    def __init__(self, config, supp_config):
        self.template = config["template"]
        self.row_count = config["row_count"]
        self.description = config["fields"]["description"]
        self.quantity = config["fields"]["quantity"]
        self.unit = config["fields"]["unit"]
        self.unit_price = config["fields"]["unit_price"]
        self.invoice_number = config["fields"]["invoice_number"]
        self.amount = config["fields"]["amount"]
        self.subtotal = config["fields"]["subtotal"]
        self.sales_tax = config["fields"]["sales_tax"]
        self.total = config["fields"]["total"]
        self.template_supp = supp_config["template"]
        self.row_count_supp = supp_config["row_count"]
        self.description_supp = supp_config["fields"]["description"]
        self.quantity_supp = supp_config["fields"]["quantity"]
        self.unit_supp = supp_config["fields"]["unit"]
        self.unit_price_supp = supp_config["fields"]["unit_price"]
        self.invoice_number_supp = supp_config["fields"]["invoice_number"]
        self.amount_supp = supp_config["fields"]["amount"]
        self.subtotal_supp = supp_config["fields"]["subtotal"]


class DailyLaborConfig:
    def __init__(self, config):
        self.template = config["template"]
        self.row_count = config["row_count"]
        self.column_count = config["fields"]["days"]["column_count"]
        self.day = config["fields"]["days"]["day"]
        self.hours_st = config["fields"]["days"]["hours_st"]
        self.hours_ot = config["fields"]["days"]["hours_ot"]
        self.classification = config["fields"]["classification"]
        self.name = config["fields"]["name"]
        self.total_st = config["fields"]["total_st"]
        self.total_ot = config["fields"]["total_ot"]


class LaborBreakdownConfig:
    def __init__(self, config, supp_config):
        self.template = config["template"]
        self.row_count = config["row_count"]
        self.base_labor_subtotal = config["base_labor_subtotal"]
        self.social_security_tax_rate = config["social_security_tax_rate"]
        self.medicare_tax_rate = config["medicare_tax_rate"]
        self.unemployment_tax_rate = config["unemployment_tax_rate"]
        self.workers_comp_insurance_rate = config["workers_comp_insurance_rate"]
        self.liability_insurance_rate = config["liability_insurance_rate"]
        self.total_taxes_and_insurance = config["total_taxes_and_insurance"]
        self.direct_labor_subtotal = config["direct_labor_subtotal"]
        self.indirect_labor_subtotal = config["indirect_labor_subtotal"]
        self.direct_labor_total = config["direct_labor_total"]
        self.indirect_labor_total = config["indirect_labor_total"]
        self.classification = config["fields"]["classification"]
        self.name = config["fields"]["name"]
        self.hours_st = config["fields"]["hours_st"]
        self.hours_ot = config["fields"]["hours_ot"]
        self.base_rate_st = config["fields"]["base_rate_st"]
        self.base_rate_ot = config["fields"]["base_rate_ot"]
        self.hw_pension_rate_st = config["fields"]["hw_pension_rate_st"]
        self.hw_pension_rate_ot = config["fields"]["hw_pension_rate_ot"]
        self.base_labor_cost_st = config["fields"]["base_labor_cost_st"]
        self.base_labor_cost_ot = config["fields"]["base_labor_cost_ot"]
        self.direct_labor_rate_st = config["fields"]["direct_labor_rate_st"]
        self.direct_labor_rate_ot = config["fields"]["direct_labor_rate_ot"]
        self.direct_labor_cost_st = config["fields"]["direct_labor_cost_st"]
        self.direct_labor_cost_ot = config["fields"]["direct_labor_cost_ot"]
        self.template_supp = supp_config["template"]
        self.row_count_supp = supp_config["row_count"]
        self.base_labor_subtotal_supp = supp_config["base_labor_subtotal"]
        self.social_security_tax_rate_supp = supp_config["social_security_tax_rate"]
        self.medicare_tax_rate_supp = supp_config["medicare_tax_rate"]
        self.unemployment_tax_rate_supp = supp_config["unemployment_tax_rate"]
        self.workers_comp_insurance_rate_supp = supp_config["workers_comp_insurance_rate"]
        self.liability_insurance_rate_supp = supp_config["liability_insurance_rate"]
        self.total_taxes_and_insurance_supp = supp_config["total_taxes_and_insurance"]
        self.direct_labor_subtotal_supp = supp_config["direct_labor_subtotal"]
        self.indirect_labor_subtotal_supp = supp_config["indirect_labor_subtotal"]
        self.classification_supp = supp_config["fields"]["classification"]
        self.name_supp = supp_config["fields"]["name"]
        self.st_hours_supp = supp_config["fields"]["hours_st"]
        self.ot_hours_supp = supp_config["fields"]["hours_ot"]
        self.base_rate_st_supp = supp_config["fields"]["base_rate_st"]
        self.base_rate_ot_supp = supp_config["fields"]["base_rate_ot"]
        self.hw_pension_rate_st_supp = supp_config["fields"]["hw_pension_rate_st"]
        self.hw_pension_rate_ot_supp = supp_config["fields"]["hw_pension_rate_ot"]
        self.base_labor_cost_st_supp = supp_config["fields"]["base_labor_cost_st"]
        self.base_labor_cost_ot_supp = supp_config["fields"]["base_labor_cost_ot"]
        self.direct_labor_rate_st_supp = supp_config["fields"]["direct_labor_rate_st"]
        self.direct_labor_rate_ot_supp = supp_config["fields"]["direct_labor_rate_ot"]
        self.direct_labor_cost_st_supp = supp_config["fields"]["direct_labor_cost_st"]
        self.direct_labor_cost_ot_supp = supp_config["fields"]["direct_labor_cost_ot"]


class EquipmentBreakdownConfig:
    def __init__(self, config, supp_config):
        self.template = config["template"]
        self.row_count = config["row_count"]
        self.amount_subtotal = config["amount_subtotal"]
        self.amount_total = config["amount_total"]
        self.description = config["fields"]["description"]
        self.year = config["fields"]["year"]
        self.h_yr = config["fields"]["h_yr"]
        self.sec_pg = config["fields"]["sec_pg"]
        self.monthly_rate = config["fields"]["monthly_rate"]
        self.equipment_adjustment = config["fields"]["equipment_adjustment"]
        self.area_adjustment = config["fields"]["area_adjustment"]
        self.adjusted_hourly_rate = config["fields"]["adjusted_hourly_rate"]
        self.operating_cost = config["fields"]["operating_cost"]
        self.total_hourly_rate_op = config["fields"]["total_hourly_rate_op"]
        self.total_hourly_rate_sb = config["fields"]["total_hourly_rate_sb"]
        self.hours_op = config["fields"]["hours_op"]
        self.hours_sb = config["fields"]["hours_sb"]
        self.amount_op = config["fields"]["amount_op"]
        self.amount_sb = config["fields"]["amount_sb"]
        self.template_supp = supp_config["template"]
        self.row_count_supp = supp_config["row_count"]
        self.amount_subtotal_supp = supp_config["amount_subtotal"]
        self.description_supp = supp_config["fields"]["description"]
        self.year_supp = supp_config["fields"]["year"]
        self.h_yr_supp = supp_config["fields"]["h_yr"]
        self.sec_pg_supp = supp_config["fields"]["sec_pg"]
        self.monthly_rate_supp = supp_config["fields"]["monthly_rate"]
        self.equipment_adjustment_supp = supp_config["fields"]["equipment_adjustment"]
        self.area_adjustment_supp = supp_config["fields"]["area_adjustment"]
        self.adjusted_hourly_rate_supp = supp_config["fields"]["adjusted_hourly_rate"]
        self.operating_cost_supp = supp_config["fields"]["operating_cost"]
        self.total_hourly_rate_op_supp = supp_config["fields"]["total_hourly_rate_op"]
        self.total_hourly_rate_sb_supp = supp_config["fields"]["total_hourly_rate_sb"]
        self.hours_op_supp = supp_config["fields"]["hours_op"]
        self.hours_sb_supp = supp_config["fields"]["hours_sb"]
        self.amount_op_supp = supp_config["fields"]["amount_op"]
        self.amount_sb_supp = supp_config["fields"]["amount_sb"]


class DailyEquipmentConfig:
    def __init__(self, config):
        self.template = config["template"]
        self.row_count = config["row_count"]
        self.column_count = config["fields"]["days"]["column_count"]
        self.day = config["fields"]["days"]["day"]
        self.hours_op = config["fields"]["days"]["hours_op"]
        self.hours_sb = config["fields"]["days"]["hours_sb"]
        self.description = config["fields"]["description"]
        self.total_op = config["fields"]["total_op"]
        self.total_sb = config["fields"]["total_sb"]


class RentalsAndServicesConfig:
    def __init__(self, config, supp_config):
        self.template = config["template"]
        self.rental_row_count = config["rental_row_count"]
        self.service_row_count = config["service_row_count"]
        self.rental_subtotal = config["rental_subtotal"]
        self.rental_total = config["rental_total"]
        self.service_subtotal = config["service_subtotal"]
        self.service_total = config["service_total"]
        self.rental_description = config["fields"]["rental_description"]
        self.rental_invoice_number = config["fields"]["rental_invoice_number"]
        self.rental_amount = config["fields"]["rental_amount"]
        self.service_description = config["fields"]["service_description"]
        self.service_invoice_number = config["fields"]["service_invoice_number"]
        self.service_amount = config["fields"]["service_amount"]
        self.template_supp = supp_config["template"]
        self.rental_row_count_supp = supp_config["rental_row_count"]
        self.service_row_count_supp = supp_config["service_row_count"]
        self.rental_subtotal_supp = supp_config["rental_subtotal"]
        self.service_subtotal_supp = supp_config["service_subtotal"]
        self.rental_description_supp = supp_config["fields"]["rental_description"]
        self.rental_invoice_number_supp = supp_config["fields"]["rental_invoice_number"]
        self.rental_amount_supp = supp_config["fields"]["rental_amount"]
        self.service_description_supp = supp_config["fields"]["service_description"]
        self.service_invoice_number_supp = supp_config["fields"]["service_invoice_number"]
        self.service_amount_supp = supp_config["fields"]["service_amount"]


class ConsumablesConfig:
    def __init__(self, config):
        self.template = config["template"]
        self.purchased_consumables_row_count = config["purchased_consumables_row_count"]
        self.stock_consumables_row_count = config["stock_consumables_row_count"]
        self.consumables_total = config["consumables_total"]
        self.purchased_consumable_description = config["fields"]["purchased_consumable_description"]
        self.purchased_consumable_quantity = config["fields"]["purchased_consumable_quantity"]
        self.purchased_consumable_unit_price = config["fields"]["purchased_consumable_unit_price"]
        self.purchased_consumable_invoice_number = config[
            "fields"]["purchased_consumable_invoice_number"]
        self.purchased_consumable_amount = config["fields"]["purchased_consumable_amount"]
        self.stock_consumable_description = config["fields"]["stock_consumable_description"]
        self.stock_consumable_invoice_value = config["fields"]["stock_consumable_invoice_value"]
        self.stock_consumable_percent_reimbursed = config[
            "fields"]["stock_consumable_percent_reimbursed"]
        self.stock_consumable_invoice_number = config["fields"]["stock_consumable_invoice_number"]
        self.stock_consumable_amount = config["fields"]["stock_consumable_amount"]


class PdfFieldConfig:
    def __init__(self, pdf_config_path):
        with open(pdf_config_path) as config_file:
            self.__config = json.load(config_file)
            self.daily_config = DailyConfig(
                self.__config["daily"], self.__config["daily_supp"])
            self.material = MaterialConfig(
                self.__config["material"], self.__config["material_supp"])
            self.final_summary = FinalSummaryConfig(
                self.__config["final_summary"])
            self.headers = HeadersConfig(
                self.__config["force_account_headers"])
            self.daily_labor = DailyLaborConfig(self.__config["daily_labor"])
            self.labor_breakdown = LaborBreakdownConfig(
                self.__config["labor_breakdown"], self.__config["labor_breakdown_supp"])
            self.equipment_breakdown = EquipmentBreakdownConfig(
                self.__config["equipment_breakdown"], self.__config["equipment_breakdown_supp"])
            self.rentals_and_services = RentalsAndServicesConfig(
                self.__config["rentals_and_services"], self.__config["rentals_and_services_supp"])
            self.consumables = ConsumablesConfig(self.__config["consumables"])
