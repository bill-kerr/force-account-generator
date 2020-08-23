from .config import Config

# COLUMNS
CHECK = Config.columns['material']['check'][0]
DESCRIPTION = Config.columns['material']['description']
QUANTITY = Config.columns['material']['quantity']
UNIT = Config.columns['material']['unit']
UNIT_PRICE = Config.columns['material']['unit_price']
INVOICE_NUMBER = Config.columns['material']['invoice_number']
SALES_TAX_RATE = Config.columns['material']['sales_tax']


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
