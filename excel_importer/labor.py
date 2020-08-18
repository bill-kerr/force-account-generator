from config import Config
from util import get_dates, get_hours

# COLUMNS
CHECK = Config.columns['labor']['check'][0]
CLASSIFICATION = Config.columns['labor']['classification']
NAME = Config.columns['labor']['name']
BASE_RATE = Config.columns['labor']['base_rate']
HW_PENSION_RATE = Config.columns['labor']['hw_pension_rate']
DATE_START = Config.columns['labor']['date_start']


def process_labor(worksheet):
    rows = worksheet.get_rows()
    labor = {key: value for key, value in worksheet.defined_cells.items()}
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
    employee['base_rate_st'] = st_row[BASE_RATE]
    employee['base_rate_ot'] = ot_row[BASE_RATE]
    employee['hw_pension_rate_st'] = st_row[HW_PENSION_RATE]
    employee['hw_pension_rate_ot'] = ot_row[HW_PENSION_RATE]
    employee['daily_hours'] = get_hours(st_row[DATE_START:], ot_row[DATE_START:], dates)
    if len(employee.get('daily_hours')) > 0:
        return employee
