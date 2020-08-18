class Page:
    def __init__(self, field_config):
        self._field_config = field_config
        self.values = {}

    def __make_field_name(self, field_name_base, row=None, column=None):
        field = field_name_base
        if row is not None:
            field += "_0" + str(row) if row < 10 else "_" + str(row)
        if column is not None:
            field += "_0" + str(column) if column < 10 else "_" + str(column)
        return field

    def _make_field(self, field_name_base, value, row=None, column=None, formatter=lambda val: str(val)):
        if not value:
            return
        key = self.__make_field_name(field_name_base, row=row, column=column)
        self.values.update({key: formatter(value)})
