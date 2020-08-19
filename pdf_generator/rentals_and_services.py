import itertools
from page import PageCollection, Page
from paginator import simple_paginate
from util import currency_formatter

class Rental:
    def __init__(self):
        self.description = ""
        self.invoice_number = ""
        self.amount = 0


class Service:
    def __init__(self):
        self.description = ""
        self.invoice_number = ""
        self.amount = 0


class RentalsAndServicesPage(Page):
    def __init__(self, rentals, services, field_config, is_first_page):
        template = field_config.template(is_supp=not is_first_page)
        super().__init__(field_config, template)
        self.__rentals = rentals
        self.__services = services
        self.__is_first_page = is_first_page
        self.rental_subtotal = 0
        self.service_subtotal = 0
        self.__calc_subtotals()
        self.__set_fields()

    def __calc_subtotals(self):
        self.__calc_rental_subtotal()
        self.__calc_service_subtotal()

    def __calc_rental_subtotal(self):
        if self.__rentals is None:
            return
        for rental in self.__rentals:
            self.rental_subtotal += rental.amount or 0

    def __calc_service_subtotal(self):
        if self.__services is None:
            return
        for service in self.__services:
            self.service_subtotal += service.amount or 0

    def __set_fields(self):
        self.__set_rental_fields()
        self.__set_service_fields()

    def __set_rental_fields(self):
        self.__set_rental_subtotal(self.rental_subtotal)
        if self.__rentals is None:
            return
        for i, rental in enumerate(self.__rentals):
            self.__set_rental_description(i + 1, rental.description)
            self.__set_rental_invoice(i + 1, rental.invoice_number)
            self.__set_rental_amount(i + 1, rental.amount)

    def __set_service_fields(self):
        self.__set_service_subtotal(self.service_subtotal)
        if self.__services is None:
            return
        for i, service in enumerate(self.__services):
            self.__set_service_description(i + 1, service.description)
            self.__set_service_invoice(i + 1, service.invoice_number)
            self.__set_service_amount(i + 1, service.amount)

    def __set_rental_subtotal(self, subtotal):
        field = self._field_config.rental_subtotal(is_supp=not self.__is_first_page)
        self.make_field(field, subtotal, formatter=currency_formatter)

    def __set_rental_description(self, row, description):
        field = self._field_config.rental_description(is_supp=not self.__is_first_page)
        self.make_field(field, description, row=row)

    def __set_rental_invoice(self, row, invoice_number):
        field = self._field_config.rental_invoice_number(is_supp=not self.__is_first_page)
        self.make_field(field, invoice_number, row=row)

    def __set_rental_amount(self, row, amount):
        field = self._field_config.rental_amount(is_supp=not self.__is_first_page)
        self.make_field(field, amount, row=row, formatter=currency_formatter)

    def __set_service_subtotal(self, subtotal):
        field = self._field_config.service_subtotal(is_supp=not self.__is_first_page)
        self.make_field(field, subtotal, formatter=currency_formatter)

    def __set_service_description(self, row, description):
        field = self._field_config.service_description(is_supp=not self.__is_first_page)
        self.make_field(field, description, row=row)

    def __set_service_invoice(self, row, invoice_number):
        field = self._field_config.service_invoice_number(is_supp=not self.__is_first_page)
        self.make_field(field, invoice_number, row=row)

    def __set_service_amount(self, row, amount):
        field = self._field_config.service_amount(is_supp=not self.__is_first_page)
        self.make_field(field, amount, row=row, formatter=currency_formatter)


class RentalsAndServicesCollection(PageCollection):
    def __init__(self, input_data, field_config):
        super().__init__(input_data, field_config)
        self.__rentals = input_data.rentals
        self.__services = input_data.services
        self.total_rental_cost = 0
        self.total_services_cost = 0
        self.__calc_totals()
        self.__paginated_rentals = simple_paginate(
            self.__rentals, self._field_config.rentals_and_services.rental_row_count())
        self.__paginated_services = simple_paginate(
            self.__services, self._field_config.rentals_and_services.service_row_count())
        self.__create_pages()
        self._populate_headers()

    def __calc_totals(self):
        for rental in self.__rentals:
            self.total_rental_cost += rental.amount or 0
        for service in self.__services:
            self.total_services_cost += service.amount or 0

    def __create_pages(self):
        if len(self.__rentals) == 0 and len(self.__services) == 0:
            return

        zipped_sets = itertools.zip_longest(self.__paginated_rentals, self.__paginated_services)
        for i, sets in enumerate(zipped_sets):
            self.pages.append(RentalsAndServicesPage(
                sets[0], sets[1], self._field_config.rentals_and_services, is_first_page=i == 0))
            if i == 0:
                self.__set_totals()

    def __set_totals(self):
        if len(self.pages) != 1:
            return
        self.pages[0].make_field(
            self._field_config.rentals_and_services.rental_total(),
            self.total_rental_cost,
            formatter=currency_formatter
        )
        self.pages[0].make_field(
            self._field_config.rentals_and_services.service_total(),
            self.total_services_cost,
            formatter=currency_formatter
        )
