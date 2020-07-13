from config import Config

# COLUMNS
R_CHECK = Config.columns['rentals_and_services']['check'][0]
R_DESCRIPTION = Config.columns['rentals_and_services']['r_description']
R_INVOICE_NUMBER = Config.columns['rentals_and_services']['r_invoice_number']
R_AMOUNT = Config.columns['rentals_and_services']['r_amount']

S_CHECK = Config.columns['rentals_and_services']['check'][1]
S_DESCRIPTION = Config.columns['rentals_and_services']['s_description']
S_INVOICE_NUMBER = Config.columns['rentals_and_services']['s_invoice_number']
S_AMOUNT = Config.columns['rentals_and_services']['s_amount']


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
