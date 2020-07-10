from config import Config

# COLUMNS
CHECK = Config.check_columns.get('services') or 0
DESCRIPTION = 7
INVOICE_NUMBER = 8
AMOUNT = 9


def process_service_sheet(worksheet):
    rows = worksheet.get_rows()
    services = []

    for row in rows:
        if row[CHECK] == 'Y':
            service = create_service_from_row(row)
            services.append(service)

    return {'data': services} if len(services) > 0 else {}


def create_service_from_row(row):
    return {
        'description': row[DESCRIPTION],
        'invoice_number': row[INVOICE_NUMBER],
        'amount': row[AMOUNT]
    }
