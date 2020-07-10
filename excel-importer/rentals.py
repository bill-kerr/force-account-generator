from config import Config

# COLUMNS
CHECK = Config.check_columns.get('rentals') or 0
DESCRIPTION = 3
INVOICE_NUMBER = 4
AMOUNT = 5


def process_rental_sheet(worksheet):
    rows = worksheet.get_rows()
    rentals = []

    for row in rows:
        if row[CHECK] == 'Y':
            rental = create_rental_from_row(row)
            rentals.append(rental)

    return {'data': rentals} if len(rentals) > 0 else {}


def create_rental_from_row(row):
    return {
        'description': row[DESCRIPTION],
        'invoice_number': row[INVOICE_NUMBER],
        'amount': row[AMOUNT]
    }
