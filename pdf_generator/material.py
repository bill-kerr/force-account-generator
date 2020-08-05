from util import paginate, get_header_fields, rnd, make_field


class Material:
    def __init__(self):
        self.description = ""
        self.quantity = 0
        self.unit = ""
        self.unit_price = 0
        self.invoice_number = ""
        self.sales_tax_rate = 0


class MaterialPage:
    def __init__(self, materials, field_config, is_first_page):
        self.is_first_page = first_page
        self.template = field_config.template
        self.materials = materials
        self.subtotal = self.__calc_subtotal()
        self.fields = field_config.material
        self.values = self.__set_fields()

    def __calc_subtotal(self):
        subtotal = 0
        for material in self.materials:
            subtotal += rnd(material.quantity * material.unit_price)
        return subtotal

    def __make_field(self, field, number, value):
        make_field(self.values, field, number, value)

    def __set_description(self, number, value):
        field = self.fields.description if self.is_first_page else self.fields.description_supp
        self.__make_field(field, number + 1, value)

    def __set_quantity(self, number, value):
        field = self.fields.quantity if self.is_first_page else self.fields.quantity_supp
        self.__make_field(field, number + 1, value)

    def __set_unit(self, number, value):
        field = self.fields.quantity if self.is_first_page else self.fields.quantity_supp

    def __set_fields(self):
        for i, material in enumerate(self.materials):
            self.__set_description(i, material.description)
            self.__set_quantity(i, material.quantity)


class MaterialCollection:
    def __init__(self, field_config, input_data):
        self.materials = input_data.material
        self.global_data = input_data.global_data
        self.field_config = field_config
        self.paginated_materials = paginate(
            self.materials, self.field_config.material.row_count)
        self.__create_pages()

    def __create_pages(self):
        if len(self.materials) == 0:
            return

        for i, materials in enumerate(self.paginated_materials):
            is_first_page = True if i == 0 else False
            page = MaterialPage(materials, self.field_config,
                                is_first_page=is_first_page)
