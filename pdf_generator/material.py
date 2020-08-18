"""
The material file includes the Material model and requisite page classes for constructing
the material portion of a force account.
"""
from util import rnd, decimal_comma_formatter, currency_formatter
from paginator import simple_paginate
from page import PageCollection, Page


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
        template = field_config.template(is_supp=not is_first_page)
        super().__init__(field_config, template)
        self.__materials = materials
        self.__is_first_page = is_first_page
        self.subtotal = self.__calc_subtotal()
        self.__set_fields()
        self.fill_blanks(
            field_config.amount(is_supp=not is_first_page),
            field_config.row_count(is_supp=not is_first_page),
            value=0,
            formatter=currency_formatter)

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
        self.__set_subtotal(self.subtotal)

    def __set_description(self, row, description):
        field = self._field_config.description(is_supp=not self.__is_first_page)
        self.make_field(field, description, row=row)

    def __set_quantity(self, row, quantity):
        field = self._field_config.quantity(is_supp=not self.__is_first_page)
        self.make_field(field, quantity, row=row)

    def __set_unit(self, row, unit):
        field = self._field_config.unit(is_supp=not self.__is_first_page)
        self.make_field(field, unit, row=row)

    def __set_unit_price(self, row, price):
        field = self._field_config.unit_price(is_supp=not self.__is_first_page)
        self.make_field(field, price, row=row, formatter=decimal_comma_formatter)

    def __set_invoice_number(self, row, invoice_number):
        field = self._field_config.invoice_number(is_supp=not self.__is_first_page)
        self.make_field(field, invoice_number, row=row)

    def __set_amount(self, row, quantity, unit_price):
        if not quantity or not unit_price:
            return
        amount = rnd(quantity * unit_price)
        field = self._field_config.amount(is_supp=not self.__is_first_page)
        self.make_field(field, amount, row=row, formatter=currency_formatter)

    def __set_subtotal(self, subtotal):
        field = self._field_config.subtotal(is_supp=not self.__is_first_page)
        self.make_field(field, subtotal, formatter=currency_formatter)


class MaterialCollection(PageCollection):
    """ The MaterialCollection class represents a set of MaterialPages. """
    def __init__(self, input_data, field_config):
        super().__init__(input_data, field_config)
        self.__materials = input_data.material
        self.__sales_tax = 0
        self.__total_cost = 0
        self.__calc_totals()
        self.__paginated_materials = simple_paginate(self.__materials, self._field_config.material.row_count())
        self.__create_pages()
        self._populate_headers()

    def __calc_totals(self):
        for material in self.__materials:
            if material.quantity is None or material.unit_price is None:
                continue
            amount = rnd(material.quantity * material.unit_price)
            tax = amount * material.sales_tax_rate
            self.__total_cost += amount + tax
            self.__sales_tax += tax

    def __create_pages(self):
        if len(self.__materials) == 0:
            return

        for i, materials in enumerate(self.__paginated_materials):
            self.pages.append(MaterialPage(materials, self._field_config.material, is_first_page=i == 0))
            if i == 0:
                self.__set_totals()

    def __set_totals(self):
        if len(self.pages) != 1:
            return
        self.pages[0].make_field(
            self._field_config.material.sales_tax(),
            self.__sales_tax,
            formatter=currency_formatter)
        self.pages[0].make_field(
            self._field_config.material.total(),
            self.__total_cost,
            formatter=currency_formatter)
