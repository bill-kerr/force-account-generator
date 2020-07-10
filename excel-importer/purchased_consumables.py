from config import Config

# COLUMNS
CHECK = Config.check_columns.get('purchased_consumables') or 0
DESCRIPTION = 3
QUANTITY = 4
UNIT_PRICE = 5
INVOICE_NUMBER = 6


def process_purchased_consumables_sheet(worksheet):
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
        'quantity': row[QUANTITY],
        'unit_price': row[UNIT_PRICE],
        'invoice_number': row[INVOICE_NUMBER]
    }
