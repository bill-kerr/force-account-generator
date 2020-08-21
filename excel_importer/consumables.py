from .config import Config

# COLUMNS
P_CHECK = Config.columns['consumables']['check'][0]
P_DESCRIPTION = Config.columns['consumables']['p_description']
P_QUANTITY = Config.columns['consumables']['p_quantity']
P_UNIT_PRICE = Config.columns['consumables']['p_unit_price']
P_INVOICE_NUMBER = Config.columns['consumables']['p_invoice_number']

S_CHECK = Config.columns['consumables']['check'][1]
S_DESCRIPTION = Config.columns['consumables']['s_description']
S_INVOICE_VALUE = Config.columns['consumables']['s_invoice_value']
S_PERCENT_REIMBURSED = Config.columns['consumables']['s_percent_reimbursed']
S_INVOICE_NUMBER = Config.columns['consumables']['s_invoice_number']


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
