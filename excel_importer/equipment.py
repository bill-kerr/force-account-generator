from .config import Config
from .util import get_dates, get_hours

# COLUMNS
CHECK = Config.columns['equipment']['check'][0]
DESCRIPTION = Config.columns['equipment']['description']
TYPE = Config.columns['equipment']['type']
CONFIGURATION = Config.columns['equipment']['configuration']
MAKE = Config.columns['equipment']['make']
MODEL = Config.columns['equipment']['model']
EQUIPMENT_NUM = Config.columns['equipment']['equipment_number']
YEAR = Config.columns['equipment']['year']
H_YR_SEC_PG = Config.columns['equipment']['h_yr_sec_pg']
MONTHLY_RATE = Config.columns['equipment']['monthly_rate']
EQUIP_ADJ = Config.columns['equipment']['equip_adj']
AREA_ADJ = Config.columns['equipment']['area_adj']
OPERATING_COST = Config.columns['equipment']['operating_cost']
DATE_START = Config.columns['equipment']['date_start']


def process_equipment(worksheet):
    rows = worksheet.get_rows()
    equipment = {}
    equipment['data'] = []
    dates = []

    for i, row in enumerate(rows):
        if row[CHECK] == 'D':
            dates = get_dates(row[DATE_START:])

        if row[CHECK] == 'Y' and row[DESCRIPTION] is not None:
            equip = create_equip_from_rows(row, rows[i + 1], dates)
            equipment['data'].append(equip)

    return {'equipment': equipment}


def create_equip_from_rows(op_row, sb_row, dates):
    equip = {}
    equip['description'] = op_row[DESCRIPTION]
    equip['year'] = op_row[YEAR]
    equip['type'] = op_row[TYPE]
    equip['configuration'] = op_row[CONFIGURATION]
    equip['make'] = op_row[MAKE]
    equip['model'] = op_row[MODEL]
    equip['equipment_number'] = op_row[EQUIPMENT_NUM]
    equip['h_yr'] = op_row[H_YR_SEC_PG]
    equip['sec_pg'] = sb_row[H_YR_SEC_PG]
    equip['monthly_rate'] = op_row[MONTHLY_RATE]
    equip['equipment_adjustment'] = op_row[EQUIP_ADJ]
    equip['area_adjustment'] = op_row[AREA_ADJ]
    equip['operating_cost'] = op_row[OPERATING_COST]
    equip['daily_hours'] = get_hours(
        op_row[DATE_START:], sb_row[DATE_START:], dates, primary_label='op', secondary_label='sb'
    )
    if len(equip.get('daily_hours')) > 0:
        return equip
