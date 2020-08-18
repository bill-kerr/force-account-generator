import json
from labor import Labor
from equipment import Equipment
from material import Material
from rental import Rental
from service import Service
from purchased_consumable import PurchasedConsumable
from stock_consumable import StockConsumable
from util import rnd


def load_material(data):
    material_list = []
    for material_data in data["data"]:
        material = Material()
        material.description = material_data["description"]
        material.quantity = material_data["quantity"]
        material.unit = material_data["unit"]
        material.unit_price = material_data["unit_price"]
        material.invoice_number = material_data["invoice_number"]
        material.sales_tax_rate = material_data["sales_tax_rate"]
        material_list.append(material)
    return material_list


def load_labor(data):
    labor_list = []
    for labor_data in data["data"]:
        labor = Labor()
        labor.classification = labor_data["classification"]
        labor.name = labor_data["name"]
        labor.base_rate_st = rnd(labor_data["base_rate_st"])
        labor.base_rate_ot = rnd(labor_data["base_rate_ot"])
        labor.hw_pension_rate_st = labor_data["hw_pension_rate_st"]
        labor.hw_pension_rate_ot = labor_data["hw_pension_rate_ot"]
        for day in labor_data["daily_hours"]:
            labor.add_daily_hours(
                day["date"], day.get("st"), day.get("ot"))

        labor_list.append(labor)

    return labor_list


def load_equipment(data):
    equip_list = []
    for equip_data in data["data"]:
        equip = Equipment()
        equip.description = equip_data["description"]
        equip.year = equip_data["year"]
        equip.type = equip_data["type"]
        equip.configuration = equip_data["configuration"]
        equip.make = equip_data["make"]
        equip.model = equip_data["model"]
        equip.equipment_number = equip_data["equipment_number"]
        equip.h_yr = equip_data["h_yr"]
        equip.sec_pg = equip_data["sec_pg"]
        equip.monthly_rate = equip_data["monthly_rate"]
        equip.equipment_adjustment = equip_data["equipment_adjustment"]
        equip.area_adjustment = equip_data["area_adjustment"]
        equip.operating_cost = equip_data["operating_cost"]
        for day in equip_data["daily_hours"]:
            equip.add_daily_hours(day["date"], day.get("op"), day.get("sb"))

        equip_list.append(equip)

    return equip_list


def load_rentals(data):
    rental_list = []
    for rental_data in data["data"]:
        rental = Rental()
        rental.description = rental_data["description"]
        rental.invoice_number = rental_data["invoice_number"]
        rental.amount = rental_data["amount"]
        rental_list.append(rental)
    return rental_list


def load_services(data):
    service_list = []
    for service_data in data["data"]:
        service = Service()
        service.description = service_data["description"]
        service.invoice_number = service_data["invoice_number"]
        service.amount = service_data["amount"]
        service_list.append(service)
    return service_list


def load_purchased_consumbles(data):
    consumable_list = []
    for consumable_data in data["data"]:
        consumable = PurchasedConsumable()
        consumable.description = consumable_data["description"]
        consumable.quantity = consumable_data["quantity"]
        consumable.unit_price = consumable_data["unit_price"]
        consumable.invoice_number = consumable_data["invoice_number"]
        consumable_list.append(consumable)
    return consumable_list


def load_stock_consumables(data):
    consumable_list = []
    for consumable_data in data["data"]:
        consumable = StockConsumable()
        consumable.description = consumable_data["description"]
        consumable.invoice_value = consumable_data["invoice_value"]
        consumable.percent_reimbursed = consumable_data["percent_reimbursed"]
        consumable.invoice_number = consumable_data["invoice_number"]
        consumable_list.append(consumable)
    return consumable_list


class GlobalData:
    def __init__(self, input_data):
        self.county = input_data["county"]
        self.state_route = input_data["state_route"]
        self.section = input_data["section"]
        self.work_order_number = input_data["work_order_number"]
        self.contract = input_data["contract"]
        self.item_number = input_data["item_number"]
        self.prime_contractor = input_data["prime_contractor"]
        self.statement_of_cost = input_data["statement_of_cost"]
        self.default_sales_tax_rate = input_data["material"]["default_sales_tax_rate"]
        self.social_security_tax_rate = input_data["labor"]["social_security_tax_rate"]
        self.medicare_tax_rate = input_data["labor"]["medicare_tax_rate"]
        self.unemployment_tax_rate = input_data["labor"]["unemployment_tax_rate"]
        self.workers_comp_insurance_rate = input_data["labor"]["workers_comp_insurance_rate"]
        self.liability_insurance_rate = input_data["labor"]["liability_insurance_rate"]


class InputData:
    def __init__(self, json_config_file):
        with open(json_config_file) as f:
            data = json.load(f)
            self.global_data = GlobalData(data)
            self.material = load_material(data["material"])
            self.labor = load_labor(data["labor"])
            self.equipment = load_equipment(data["equipment"])
            self.rentals = load_rentals(data["rentals"])
            self.services = load_services(data["services"])
            self.purchased_consumables = load_purchased_consumbles(
                data["purchased_consumables"])
            self.stock_consumables = load_stock_consumables(
                data["stock_consumables"])
