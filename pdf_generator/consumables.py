from itertools import zip_longest
from page import PageCollection, Page
from paginator import simple_paginate
from util import currency_formatter, decimal_comma_formatter, three_decimal_formatter, two_decimal_percent_formatter

class PurchasedConsumable:
    def __init__(self):
        self.description = ""
        self.quantity = 0
        self.unit_price = 0
        self.invoice_number = ""

    @property
    def amount(self):
        return self.quantity * self.unit_price


class StockConsumable:
    def __init__(self):
        self.description = ""
        self.invoice_value = 0
        self.percent_reimbursed = 0
        self.invoice_number = ""

    @property
    def amount(self):
        return self.invoice_value * self.percent_reimbursed


class ConsumablesPage(Page):
    def __init__(self, purchased, stock, field_config):
        template = field_config.template()
        super().__init__(field_config, template)
        self.__purchased = purchased
        self.__stock = stock
        self.purchased_subtotal = 0
        self.stock_subtotal = 0
        self.total_cost = 0
        self.__calc_totals()
        self.__set_fields()
        self.__fill_blanks()

    def __calc_totals(self):
        self.__calc_purchased_subtotal()
        self.__calc_stock_subtotal()
        self.total_cost = self.purchased_subtotal + self.stock_subtotal

    def __calc_purchased_subtotal(self):
        if self.__purchased is None:
            return
        for consumable in self.__purchased:
            self.purchased_subtotal += consumable.amount

    def __calc_stock_subtotal(self):
        if self.__stock is None:
            return
        for consumable in self.__stock:
            self.stock_subtotal += consumable.amount

    def __set_fields(self):
        self.__set_purchased_fields()
        self.__set_stock_fields()
        self.__set_total(self.total_cost)

    def __set_purchased_fields(self):
        self.__set_purchased_subtotal(self.purchased_subtotal)
        if self.__purchased is None:
            return
        for i, consumable in enumerate(self.__purchased):
            self.__set_purchased_description(i + 1, consumable.description)
            self.__set_purchased_quantity(i + 1, consumable.quantity)
            self.__set_purchased_unit_price(i + 1, consumable.unit_price)
            self.__set_purchased_invoice(i + 1, consumable.invoice_number)
            self.__set_purchased_amount(i + 1, consumable.amount)

    def __set_stock_fields(self):
        self.__set_stock_subtotal(self.stock_subtotal)
        if self.__stock is None:
            return
        for i, consumable in enumerate(self.__stock):
            self.__set_stock_description(i + 1, consumable.description)
            self.__set_stock_invoice_value(i + 1, consumable.invoice_value)
            self.__set_stock_percent_reimbursed(i + 1, consumable.percent_reimbursed)
            self.__set_stock_invoice(i + 1, consumable.invoice_number)
            self.__set_stock_amount(i + 1, consumable.amount)

    def __set_total(self, total):
        field = self._field_config.consumables_total()
        self.make_field(field, total, formatter=currency_formatter)

    def __set_purchased_subtotal(self, subtotal):
        field = self._field_config.purchased_consumable_subtotal()
        self.make_field(field, subtotal, formatter=currency_formatter)

    def __set_purchased_description(self, row, description):
        field = self._field_config.purchased_consumable_description()
        self.make_field(field, description, row=row)

    def __set_purchased_quantity(self, row, quantity):
        field = self._field_config.purchased_consumable_quantity()
        self.make_field(field, quantity, row=row, formatter=three_decimal_formatter)

    def __set_purchased_unit_price(self, row, unit_price):
        field = self._field_config.purchased_consumable_unit_price()
        self.make_field(field, unit_price, row=row, formatter=decimal_comma_formatter)

    def __set_purchased_invoice(self, row, invoice_number):
        field = self._field_config.purchased_consumable_invoice_number()
        self.make_field(field, invoice_number, row=row)

    def __set_purchased_amount(self, row, amount):
        field = self._field_config.purchased_consumable_amount()
        self.make_field(field, amount, row=row, formatter=currency_formatter)

    def __set_stock_subtotal(self, subtotal):
        field = self._field_config.stock_consumable_subtotal()
        self.make_field(field, subtotal, formatter=currency_formatter)

    def __set_stock_description(self, row, description):
        field = self._field_config.stock_consumable_description()
        self.make_field(field, description, row=row)

    def __set_stock_invoice_value(self, row, value):
        field = self._field_config.stock_consumable_invoice_value()
        self.make_field(field, value, row=row, formatter=decimal_comma_formatter)

    def __set_stock_percent_reimbursed(self, row, percent):
        field = self._field_config.stock_consumable_percent_reimbursed()
        self.make_field(field, percent, row=row, formatter=two_decimal_percent_formatter)

    def __set_stock_invoice(self, row, invoice_number):
        field = self._field_config.stock_consumable_invoice_number()
        self.make_field(field, invoice_number, row=row)

    def __set_stock_amount(self, row, amount):
        field = self._field_config.stock_consumable_amount()
        self.make_field(field, amount, row=row, formatter=currency_formatter)

    def __fill_blanks(self):
        self.fill_blanks(
            self._field_config.purchased_consumable_amount(),
            self._field_config.purchased_consumables_row_count(),
            value=0,
            formatter=currency_formatter)
        self.fill_blanks(
            self._field_config.stock_consumable_amount(),
            self._field_config.stock_consumables_row_count(),
            value=0,
            formatter=currency_formatter)
        self.fill_blanks(
            self._field_config.stock_consumable_percent_reimbursed(),
            self._field_config.stock_consumables_row_count(),
            value=0,
            formatter=two_decimal_percent_formatter)


class ConsumablesCollection(PageCollection):
    def __init__(self, data_loader, field_config):
        super().__init__(data_loader, field_config)
        self.__purchased = data_loader.purchased_consumables
        self.__stock = data_loader.stock_consumables
        self.total_consumables_cost = 0
        self.__calc_totals()
        self.__paginated_purchased = simple_paginate(
            self.__purchased, self._field_config.consumables.purchased_consumables_row_count())
        self.__paginated_stock = simple_paginate(
            self.__stock, self._field_config.consumables.stock_consumables_row_count())
        self.__create_pages()
        self._populate_headers()

    def __calc_totals(self):
        for item in self.__purchased:
            self.total_consumables_cost += item.amount or 0
        for item in self.__stock:
            self.total_consumables_cost += item.amount or 0

    def __create_pages(self):
        if len(self.__purchased) == 0 and len(self.__stock) == 0:
            return

        zipped_sets = zip_longest(self.__paginated_purchased, self.__paginated_stock)
        for sets in zipped_sets:
            self.pages.append(ConsumablesPage(sets[0], sets[1], self._field_config.consumables))
