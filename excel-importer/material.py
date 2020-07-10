from config import config

# COLUMNS
CHECK = 0
DESCRIPTION = 1
QUANTITY = 2
UNIT = 3
UNIT_PRICE = 4
INVOICE_NUMBER = 5
SALES_TAX_RATE = 7


def process_material_sheet(worksheet):
    rows = worksheet.get_rows()
    materials = []
    cell_name = config['defined_cells']['sales_tax']
    default_sales_tax = worksheet.defined_cells[cell_name]

    for row in rows:
        material = create_material_from_row(row, default_sales_tax)
        materials.append(material)

    return {
        'default_sales_tax_rate': default_sales_tax,
        'data': materials
    } if len(materials) > 0 else {}


def create_material_from_row(row, default_sales_tax):
    if row[0] == 'Y':
        return {
            'description': row[DESCRIPTION],
            'quantity': row[QUANTITY],
            'unit': row[UNIT],
            'unit_price': row[UNIT_PRICE],
            'invoice_number': row[INVOICE_NUMBER],
            'sales_tax_rate': row[SALES_TAX_RATE] if row[SALES_TAX_RATE] is not None else default_sales_tax
        }
