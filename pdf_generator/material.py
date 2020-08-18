"""
The material file includes the Material model and requisite page classes for constructing
the material portion of a force account.
"""
from util import rnd, decimal_comma_formatter, currency_formatter
from paginator import simple_paginate
from page import Page


class Material:
    """ The Material class represents a single material object. """
    def __init__(self):
        self.description = ""
        self.quantity = 0
        self.unit = ""
        self.unit_price = 0
        self.invoice_number = ""
        self.sales_tax_rate = 0


class MaterialPage(Page):
    """ The MaterialPage class represents a single material page. """
    def __init__(self, materials, field_config, is_first_page):
        super().__init__(field_config)
        self.__materials = materials
        self.__is_first_page = is_first_page
        self.__subtotal = self.__calc_subtotal()
        self.__set_fields()

    def __calc_subtotal(self):
        subtotal = 0
        for material in self.__materials:
            if material.quantity is None or material.unit_price is None:
                continue
            subtotal += rnd(material.quantity * material.unit_price)
        return subtotal

    def __set_fields(self):
        for i, material in enumerate(self.__materials):
            self.__set_description(i + 1, material.description)
            self.__set_quantity(i + 1, material.quantity)
            self.__set_unit(i + 1, material.unit)
            self.__set_unit_price(i + 1, material.unit_price)
            self.__set_invoice_number(i + 1, material.invoice_number)
            self.__set_amount(i + 1, material.quantity, material.unit_price)

    def __set_description(self, row, description):
        field = self._field_config.description(is_supp=not self.__is_first_page)
        self._make_field(field, description, row=row)

    def __set_quantity(self, row, quantity):
        field = self._field_config.quantity(is_supp=not self.__is_first_page)
        self._make_field(field, quantity, row=row)

    def __set_unit(self, row, unit):
        field = self._field_config.unit(is_supp=not self.__is_first_page)
        self._make_field(field, unit, row=row)

    def __set_unit_price(self, row, price):
        field = self._field_config.unit_price(is_supp=not self.__is_first_page)
        self._make_field(field, price, row=row, formatter=decimal_comma_formatter)

    def __set_invoice_number(self, row, invoice_number):
        field = self._field_config.invoice_number(is_supp=not self.__is_first_page)
        self._make_field(field, invoice_number, row=row)

    def __set_amount(self, row, quantity, unit_price):
        if not quantity or not unit_price:
            return
        amount = rnd(quantity * unit_price)
        field = self._field_config.amount(is_supp=not self.__is_first_page)
        self._make_field(field, amount, row=row, formatter=currency_formatter)


class MaterialCollection:
    """ The MaterialCollection class represents a set of MaterialPages. """
    def __init__(self, field_config, input_data):
        self.materials = input_data.material
        self.global_data = input_data.global_data
        self.field_config = field_config
        self.paginated_materials = simple_paginate(self.materials, self.field_config.material.row_count())
        self.__create_pages()

    def __create_pages(self):
        if len(self.materials) == 0:
            return

        pages = []
        for i, materials in enumerate(self.paginated_materials):
            pages.append(MaterialPage(materials, self.field_config.material, is_first_page=i == 0))
