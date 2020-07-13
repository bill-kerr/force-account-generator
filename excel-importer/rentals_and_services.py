from config import Config

# COLUMNS
R_CHECK = Config.check_columns.get('rentals_and_services')[0] or 0
R_DESCRIPTION = 3
R_INVOICE_NUMBER = 4
R_AMOUNT = 5

S_CHECK = Config.check_columns.get('rentals_and_services')[1] or 0
S_DESCRIPTION = 7
S_INVOICE_NUMBER = 8
S_AMOUNT = 9


def process_rentals_and_services(worksheet):
    rows = worksheet.get_rows()
    rentals = []
    services = []

    for row in rows:
        if row[R_CHECK] == 'Y':
            rental = create_rental_from_row(row)
            rentals.append(rental)
        if row[S_CHECK] == 'Y':
            service = create_service_from_row(row)
            services.append(service)

    data = {}
    data['rentals'] = {'data': rentals}
    data['services'] = {'data': services}
    return data


def create_rental_from_row(row):
    return {
        'description': row[R_DESCRIPTION],
        'invoice_number': row[R_INVOICE_NUMBER],
        'amount': row[R_AMOUNT]
    }


def create_service_from_row(row):
    return {
        'description': row[S_DESCRIPTION],
        'invoice_number': row[S_INVOICE_NUMBER],
        'amount': row[S_AMOUNT]
    }
