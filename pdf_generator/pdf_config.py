import json


class DailyConfig:
    def __init__(self, daily_config, daily_supp_config):
        self.__daily_config = daily_config
        self.__daily_supp_config = daily_supp_config

    @property
    def template(self):
        return self.__daily_config["template"]

    @property
    def description(self):
        return self.__daily_config["description"]

    @property
    def date(self):
        return self.__daily_config["date"]

    @property
    def ecms_number(self):
        return self.__daily_config["ecms_number"]

    @property
    def sr_sec(self):
        return self.__daily_config["sr_sec"]

    @property
    def item_number(self):
        return self.__daily_config["item_number"]

    @property
    def authorization_number(self):
        return self.__daily_config["authorization_no"]

    @property
    def contractor(self):
        return self.__daily_config["contractor"]

    @property
    def subcontractor(self):
        return self.__daily_config["subcontractor"]

    @property
    def inspector(self):
        return self.__daily_config["inspector"]

    @property
    def locations(self):
        return self.__daily_config["locations"]

    @property
    def labor_row_count(self):
        return self.__daily_config["labor"]["row_count"]

    @property
    def labor_name(self):
        return self.__daily_config["labor"]["fields"]["name"]

    @property
    def labor_classification(self):
        return self.__daily_config["labor"]["fields"]["classification"]

    @property
    def labor_hours_st(self):
        return self.__daily_config["labor"]["fields"]["hours_st"]

    @property
    def labor_hours_ot(self):
        return self.__daily_config["labor"]["fields"]["hours_ot"]

    @property
    def equipment_row_count(self):
        return self.__daily_config["equipment"]["row_count"]

    @property
    def equipment_type(self):
        return self.__daily_config["equipment"]["fields"]["equipment_type"]

    @property
    def equipment_configuration(self):
        return self.__daily_config["equipment"]["fields"]["configuration"]

    @property
    def equipment_year(self):
        return self.__daily_config["equipment"]["fields"]["year"]

    @property
    def equipment_make(self):
        return self.__daily_config["equipment"]["fields"]["make"]

    @property
    def equipment_model(self):
        return self.__daily_config["equipment"]["fields"]["model"]

    @property
    def equipment_hours_op(self):
        return self.__daily_config["equipment"]["fields"]["hours_op"]

    @property
    def equipment_hours_sb(self):
        return self.__daily_config["equipment"]["fields"]["hours_sb"]

    @property
    def template_supp(self):
        return self.__daily_supp_config["template"]

    @property
    def description_supp(self):
        return self.__daily_supp_config["description"]

    @property
    def date_supp(self):
        return self.__daily_supp_config["date"]

    @property
    def ecms_number_supp(self):
        return self.__daily_supp_config["ecms_number"]

    @property
    def sr_sec_supp(self):
        return self.__daily_supp_config["sr_sec"]

    @property
    def item_number_supp(self):
        return self.__daily_supp_config["item_number"]

    @property
    def authorization_number_supp(self):
        return self.__daily_supp_config["authorization_no"]

    @property
    def contractor_supp(self):
        return self.__daily_supp_config["contractor"]

    @property
    def subcontractor_supp(self):
        return self.__daily_supp_config["subcontractor"]

    @property
    def inspector_supp(self):
        return self.__daily_supp_config["inspector"]

    @property
    def locations_supp(self):
        return self.__daily_supp_config["locations"]


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
        self.template_supp = supp_config[""]
        self.row_count_supp = supp_config["row_count"]
        self.description_supp = supp_config["fields"]["description"]
        self.quantity_supp = supp_config["fields"]["quantity"]
        self.unit_supp = supp_config["fields"]["unit"]
        self.unit_price_supp = supp_config["fields"]["unit_price"]
        self.invoice_number_supp = supp_config["fields"]["invoice_number"]
        self.amount_supp = supp_config["fields"]["amount"]
        self.subtotal_supp = supp_config["fields"]["subtotal"]


class PdfConfig:
    def __init__(self, pdf_config_path):
        with open(pdf_config_path) as config_file:
            self.__config = json.load(config_file)
            self.daily_config = DailyConfig(
                self.__config["daily"], self.__config["daily_supp"])
            self.material = MaterialConfig(
                self.__config["material"], self.__config["material_supp"])
