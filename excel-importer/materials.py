from config import Config

# COLUMNS
CHECK = Config.check_columns.get('material')[0] or 0
DESCRIPTION = 1
QUANTITY = 2
UNIT = 3
UNIT_PRICE = 4
INVOICE_NUMBER = 5
SALES_TAX_RATE = 7


def process_material(worksheet):
    rows = worksheet.get_rows()
    materials = []
    default_sales_tax = worksheet.defined_cells['sales_tax']

    for row in rows:
        if row[CHECK] == 'Y':
            material = create_material_from_row(row, default_sales_tax)
            materials.append(material)

    material = {}
    material['default_sales_tax_rate'] = default_sales_tax
    material['data'] = materials
    return {'material': material}


def create_material_from_row(row, default_sales_tax):
    return {
        'description': row[DESCRIPTION],
        'quantity': row[QUANTITY],
        'unit': row[UNIT],
        'unit_price': row[UNIT_PRICE],
        'invoice_number': row[INVOICE_NUMBER],
        'sales_tax_rate': row[SALES_TAX_RATE] if row[SALES_TAX_RATE] is not None else default_sales_tax
    }
