from util import make_field
from pdf_config import PdfConfig


class DailyPage:
    def __init__(self, template, labor, equipment):
        self.__labor = labor
        self.__equipment = equipment
        self.template = template
        pdf_config = PdfConfig()
        self.__config = pdf_config.daily_config
        self.fields = {}
        self.__fill_fields()

    def __fill_fields(self):
        self.__fill_meta_fields()
        self.__fill_labor_fields()
        self.__fill_equipment_fields()

    def __fill_meta_fields(self):
        self.fields[self.__config.date] =

    def __fill_labor_fields(self):
        for i, labor in enumerate(self.__labor):
            make_field(self.fields, self.__config.labor_name,
                       i + 1, labor["unit"]["name"])
            make_field(self.fields, self.__config.labor_classification,
                       i + 1, labor["unit"]["classification"])
            make_field(self.fields, self.__config.labor_hours_st,
                       i + 1, labor["st"])
            make_field(self.fields, self.__config.labor_hours_ot,
                       i + 1, labor["ot"])

    def __fill_equipment_fields(self):
        for i, equip in enumerate(self.__equipment):
            make_field(self.fields, self.__config.equipment_type,
                       i + 1, equip["unit"]["type"])
            make_field(self.fields, self.__config.equipment_configuration,
                       i + 1, equip["unit"]["configuration"])
            make_field(self.fields, self.__config.equipment_year,
                       i + 1, equip["unit"]["year"])
            make_field(self.fields, self.__config.equipment_make,
                       i + 1, equip["unit"]["make"])
            make_field(self.fields, self.__config.equipment_model,
                       i + 1, equip["unit"]["model"])
            make_field(self.fields,
                       self.__config.equipment_hours_op, i + 1, equip["op"])
            make_field(self.fields,
                       self.__config.equipment_hours_sb, i + 1, equip["sb"])
