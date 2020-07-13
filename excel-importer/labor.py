from config import Config
from util import get_dates, get_hours

# COLUMNS
CHECK = Config.check_columns.get('labor')[0] or 0
CLASSIFICATION = 1
NAME = 2
BASE_RATE = 3
HW_PENSION_RATE = 4
DATE_START = 10


def process_labor(worksheet):
    rows = worksheet.get_rows()
    defined_cell_names = Config.defined_cells
    labor = {}
    labor['social_security_tax_rate'] = worksheet.defined_cells['social_security_tax_rate']
    labor['medicare_tax_rate'] = worksheet.defined_cells['medicare_tax_rate']
    labor['unemployment_tax_rate'] = worksheet.defined_cells['unemployment_tax_rate']
    labor['workers_comp_insurance_rate'] = worksheet.defined_cells['workers_comp_insurance_rate']
    labor['liability_insurance_rate'] = worksheet.defined_cells['liability_insurance_rate']
    labor['data'] = []
    dates = []

    for i, row in enumerate(rows):
        if row[CHECK] == 'D':
            dates = get_dates(row[DATE_START:])

        if row[CHECK] == 'Y' and row[CLASSIFICATION] is not None:
            employee = create_employee_from_rows(row, rows[i + 1], dates)
            labor['data'].append(employee)

    return {'labor': labor}


def create_employee_from_rows(st_row, ot_row, dates):
    employee = {}
    employee['classification'] = st_row[CLASSIFICATION]
    employee['name'] = st_row[NAME]
    employee['base_rate'] = st_row[BASE_RATE]
    employee['hw_pension_rate'] = st_row[HW_PENSION_RATE]
    employee['daily_hours'] = get_hours(st_row[DATE_START:], ot_row[DATE_START:], dates)
    if len(employee.get('daily_hours')) > 0:
        return employee
