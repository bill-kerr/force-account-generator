from config import Config

# COLUMNS
CHECK = Config.check_columns.get('stock_consumables') or 0
DESCRIPTION = 9
INVOICE_VALUE = 10
PERCENT_REIMBURSED = 11
INVOICE_NUMBER = 12


def process_stock_consumables_sheet(worksheet):
    rows = worksheet.get_rows()
    consumables = []

    for row in rows:
        if row[CHECK] == 'Y':
            consumable = create_consumable_from_row(row)
            consumables.append(consumable)

    return {'data': consumables} if len(consumables) > 0 else {}


def create_consumable_from_row(row):
    return {
        'description': row[DESCRIPTION],
        'invoice_value': row[INVOICE_VALUE],
        'percent_reimbursed': row[PERCENT_REIMBURSED],
        'invoice_number': row[INVOICE_NUMBER]
    }
