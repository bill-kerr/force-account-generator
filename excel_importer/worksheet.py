from config import Config


class Worksheet:
    def __init__(self, worksheet, defined_cells, process):
        self._worksheet = worksheet
        self._set_name()
        self.defined_cells = defined_cells
        self._load_rows()
        self._process = process

    def __repr__(self):
        return 'Worksheet(' + self.name + ')'

    def _set_name(self):
        org_name = self._worksheet.title
        for name, org in Config.worksheet_names.items():
            if org_name == org:
                self.name = name
                return

    def _load_rows(self):
        self._rows = []
        self.has_data = False
        cols = Config.columns.get(self.name)
        check_cols = cols['check'] if cols else None
        if not check_cols:
            return

        for row in self._worksheet.rows:
            use_row = False
            for col in check_cols:
                if self._check_for_data(row[col]):
                    use_row = True
                    break

            if use_row:
                self._rows.append([])
                self._load_cells(row)

    def _check_for_data(self, cell):
        if not self.has_data and cell.value == 'Y':
            self.has_data = True

        if cell.value != 'N':
            return True
        return False

    def _load_cells(self, row):
        for cell in row:
            self._rows[-1].append(cell.value)

    def cell_value(self, cell_coordinates):
        return self._worksheet[cell_coordinates].value

    def get_rows(self):
        return self._rows

    def process(self):
        return self._process(self) if self._process else {}
