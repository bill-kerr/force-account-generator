from config import config

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
  }

def create_material_from_row(row, default_sales_tax):
  return {
    'description': row[1],
    'quantity': row[2],
    'unit': row[3],
    'unit_price': row[4],
    'invoice_number': row[5],
    'sales_tax_rate': row[7] if row[7] is not None else default_sales_tax
  }