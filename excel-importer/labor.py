from config import config

# COLUMNS
CHECK = 0
CLASSIFICATION = 1
NAME = 2
BASE_RATE = 3
HW_PENSION_RATE = 4
DATE_START = 10


def process_labor_sheet(worksheet):
    rows = worksheet.get_rows()
    defined_cell_names = config['defined_cells']
    labor = {}
    labor['social_security_tax_rate'] = worksheet.defined_cells[defined_cell_names['social_security_tax_rate']]
    labor['medicare_tax_rate'] = worksheet.defined_cells[defined_cell_names['medicare_tax_rate']]
    labor['unemployment_tax_rate'] = worksheet.defined_cells[defined_cell_names['unemployment_tax_rate']]
    labor['workers_comp_insurance_rate'] = worksheet.defined_cells[defined_cell_names['workers_comp_insurance_rate']]
    labor['liability_insurance_rate'] = worksheet.defined_cells[defined_cell_names['liability_insurance_rate']]
    labor['data'] = []
    dates = []

    for i, row in enumerate(rows):
        if row[CHECK] == 'D':
            dates = get_dates(row[DATE_START:])

        if row[CHECK] == 'Y' and row[CLASSIFICATION] is not None:
            employee = create_employee_from_rows(row, rows[i + 1], dates)
            labor['data'].append(employee)

    return labor


def get_dates(row):
    dates = []
    for value in row:
        dates.append(value.strftime('%Y-%m-%d') if value is not None else None)
    return dates


def create_employee_from_rows(st_row, ot_row, dates):
    employee = {}
    employee['classification'] = st_row[CLASSIFICATION]
    employee['name'] = st_row[NAME]
    employee['base_rate'] = st_row[BASE_RATE]
    employee['hw_pension_rate'] = st_row[HW_PENSION_RATE]
    employee['daily_hours'] = get_hours(st_row[DATE_START:], ot_row[DATE_START:], dates)
    if len(employee.get('daily_hours')) > 0:
        return employee


def get_hours(st_row, ot_row, dates):
    daily_hours = []
    for st, ot, date in zip(st_row, ot_row, dates):
        if date is None or (st is None and ot is None):
            continue

        hours = {
            'date': date
        }
        if st is not None:
            hours['st'] = st
        if ot is not None:
            hours['ot'] = ot
        daily_hours.append(hours)

    return daily_hours
