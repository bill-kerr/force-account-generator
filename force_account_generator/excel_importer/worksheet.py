from .config import Config


class Worksheet:
    def __init__(self, worksheet, defined_cells, process):
        self.__worksheet = worksheet
        self.__set_name()
        self.defined_cells = defined_cells
        self.__load_rows()
        self.__process = process

    def __repr__(self):
        return 'Worksheet(' + self.name + ')'

    def _set_name(self):
        org_name = self.__worksheet.title
        for name, org in Config.worksheet_names.items():
            if org_name == org:
                self.name = name
                return

    def __load_rows(self):
        self.__rows = []
        self.has_data = False
        cols = Config.columns.get(self.name)
        check_cols = cols['check'] if cols else None
        if not check_cols:
            return

        for row in self.__worksheet.rows:
            use_row = False
            for col in check_cols:
                if self.__check_for_data(row[col]):
                    use_row = True
                    break

            if use_row:
                self.__rows.append([])
                self.__load_cells(row)

    def __check_for_data(self, cell):
        if not self.has_data and cell.value == 'Y':
            self.has_data = True

        if cell.value != 'N':
            return True
        return False

    def __load_cells(self, row):
        for cell in row:
            self.__rows[-1].append(cell.value)

    def cell_value(self, cell_coordinates):
        return self.__worksheet[cell_coordinates].value

    def get_rows(self):
        return self.__rows

    def process(self):
        return self.__process(self) if self.__process else {}
