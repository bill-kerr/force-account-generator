"""
The material file includes the Material model and requisite page classes for constructing
the material portion of a force account.
"""
from util import rnd, make_field
from paginator import simple_paginate


class Material:
    """ The Material class represents a single material object. """
    def __init__(self):
        self.description = ""
        self.quantity = 0
        self.unit = ""
        self.unit_price = 0
        self.invoice_number = ""
        self.sales_tax_rate = 0


class MaterialPage:
    """ The MaterialPage class represents a single material page. """
    def __init__(self, materials, field_config, is_first_page):
        self.materials = materials
        self.field_config = field_config
        self.is_first_page = is_first_page
        self.values = {}
        self.subtotal = self.__calc_subtotal()
        self.__set_fields()

    def __calc_subtotal(self):
        subtotal = 0
        for material in self.materials:
            if material.quantity is None or material.unit_price is None:
                continue
            subtotal += rnd(material.quantity * material.unit_price)
        return subtotal

    def __set_fields(self):
        for i, material in enumerate(self.materials):
            self.__set_description(i, material.description)
            self.__set_quantity(i, material.quantity)
            self.__set_unit(i, material.unit)
            self.__set_unit_price(i, material.unit_price)
            self.__set_invoice_number(i, material.invoice_number)
            self.__set_amount(i, material.quantity, material.unit_price)

    def __make_field(self, field, number, value):
        if not value:
            return
        value = str(value)
        make_field(self.values, field, number + 1, value)

    def __set_description(self, number, value):
        field = self.field_config.description(is_supp=not self.is_first_page)
        self.__make_field(field, number, value)

    def __set_quantity(self, number, value):
        field = self.field_config.quantity(is_supp=not self.is_first_page)
        self.__make_field(field, number, value)

    def __set_unit(self, number, value):
        field = self.field_config.unit(is_supp=not self.is_first_page)
        self.__make_field(field, number, value)

    def __set_unit_price(self, number, value):
        if not value:
            return
        field = self.field_config.unit_price(is_supp=not self.is_first_page)
        self.__make_field(field, number, f'{value:,.2f}')

    def __set_invoice_number(self, number, value):
        field = self.field_config.invoice_number(is_supp=not self.is_first_page)
        self.__make_field(field, number, value)

    def __set_amount(self, number, quantity, unit_price):
        if not quantity or not unit_price:
            return
        amount = quantity * unit_price
        field = self.field_config.amount(is_supp=not self.is_first_page)
        self.__make_field(field, number, f'$ {amount:,.2f}')


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
