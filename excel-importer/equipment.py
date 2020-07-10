from config import config
from util import get_dates, get_hours

# COLUMNS
CHECK = 0
DESCRIPTION = 2
YEAR = 3
H_YR_SEC_PG = 4
MONTHLY_RATE = 5
EQUIP_ADJ = 6
AREA_ADJ = 7
OPERATING_COST = 8
DATE_START = 14


def process_equipment_sheet(worksheet):
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

    return equipment if len(equipment['data']) > 0 else {}


def create_equip_from_rows(ot_row, sb_row, dates):
    equip = {}
    equip['description'] = ot_row[DESCRIPTION]
    equip['year'] = ot_row[YEAR]
    equip['h_yr'] = ot_row[H_YR_SEC_PG]
    equip['sec_pg'] = sb_row[H_YR_SEC_PG]
    equip['monthly_rate'] = ot_row[MONTHLY_RATE]
    equip['equipment_adjustment'] = ot_row[EQUIP_ADJ]
    equip['area_adjustment'] = ot_row[AREA_ADJ]
    equip['operating_cost'] = ot_row[OPERATING_COST]
    equip['daily_hours'] = get_hours(
        ot_row[DATE_START:], sb_row[DATE_START:], dates, primary_label='ot', secondary_label='sb'
    )
    if len(equip.get('daily_hours')) > 0:
        return equip
