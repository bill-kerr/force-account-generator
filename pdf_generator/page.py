class Page:
    def __init__(self, field_config, template):
        self._field_config = field_config
        self.template = template
        self.values = {}

    def __make_field_name(self, field_name_base, row=None, column=None):
        field = field_name_base
        if row is not None:
            field += "_0" + str(row) if row < 10 else "_" + str(row)
        if column is not None:
            field += "_0" + str(column) if column < 10 else "_" + str(column)
        return field

    def make_field(self, field_name_base, value, row=None, column=None, formatter=lambda val: str(val)):
        if value is None:
            return
        key = self.__make_field_name(field_name_base, row=row, column=column)
        self.values.update({key: formatter(value)})
    
    def fill_blanks(self, field_name_base, row_count, value="", formatter=lambda val: str(val)):
        for i in range(row_count):
            field_name = self.__make_field_name(field_name_base, row=i + 1)
            if field_name not in self.values:
                self.make_field(field_name_base, value, row=i + 1, formatter=formatter)


class PageCollection:
    def __init__(self, data_loader, field_config):
        self._global_data = data_loader.global_data
        self._field_config = field_config
        self.pages = []

    def _populate_headers(self):
        config = self._field_config.headers
        for page in self.pages:
            page.make_field(config.county, self._global_data.county)
            page.make_field(config.state_route, self._global_data.state_route)
            page.make_field(config.section, self._global_data.section)
            page.make_field(config.work_order_number, self._global_data.work_order_number)
            page.make_field(config.contract, self._global_data.contract)
            page.make_field(config.item_number, self._global_data.item_number)


def populate_page_headers(page, pdf_config, global_data):
    config = pdf_config.headers
    page.make_field(config.county, global_data.county)
    page.make_field(config.state_route, global_data.state_route)
    page.make_field(config.section, global_data.section)
    page.make_field(config.work_order_number, global_data.work_order_number)
    page.make_field(config.contract, global_data.contract)
    page.make_field(config.item_number, global_data.item_number)
