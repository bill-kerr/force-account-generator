from config import Config

# COLUMNS
P_CHECK = Config.check_columns.get('consumables')[0] or 0
P_DESCRIPTION = 3
P_QUANTITY = 4
P_UNIT_PRICE = 5
P_INVOICE_NUMBER = 6

S_CHECK = Config.check_columns.get('consumables')[1] or 1
S_DESCRIPTION = 9
S_INVOICE_VALUE = 10
S_PERCENT_REIMBURSED = 11
S_INVOICE_NUMBER = 12


def process_consumables(worksheet):
    rows = worksheet.get_rows()
    purchased = []
    stock = []

    for row in rows:
        if row[P_CHECK] == 'Y':
            consumable = create_purchased_from_row(row)
            purchased.append(consumable)
        if row[S_CHECK] == 'Y':
            consumable = create_stock_from_row(row)
            stock.append(consumable)

    data = {}
    data['purchased_consumables'] = {'data': purchased}
    data['stock_consumables'] = {'data': stock}
    return data


def create_purchased_from_row(row):
    return {
        'description': row[P_DESCRIPTION],
        'quantity': row[P_QUANTITY],
        'unit_price': row[P_UNIT_PRICE],
        'invoice_number': row[P_INVOICE_NUMBER]
    }


def create_stock_from_row(row):
    return {
        'description': row[S_DESCRIPTION],
        'invoice_value': row[S_INVOICE_VALUE],
        'percent_reimbursed': row[S_PERCENT_REIMBURSED],
        'invoice_number': row[S_INVOICE_NUMBER]
    }
