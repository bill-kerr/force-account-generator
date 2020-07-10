class Worksheet:
    def __init__(self, worksheet, defined_cells):
        self.__worksheet = worksheet
        self.worksheet_name = self.__worksheet.title
        self.defined_cells = defined_cells
        self.__load_rows()

    def __repr__(self):
        return 'Worksheet(' + self.worksheet_name + ')'

    def __load_rows(self):
        self.__rows = []
        for row in self.__worksheet.rows:
            if row[0].value == 'Y':
                self.__rows.append([])
                self.__load_cells(row)

    def __load_cells(self, row):
        for cell in row:
            self.__rows[-1].append(cell.value)

    def cell_value(self, cell_coordinates):
        return self.__worksheet[cell_coordinates].value

    def get_rows(self):
        return self.__rows
