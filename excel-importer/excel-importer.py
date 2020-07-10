from workbook import Workbook
from material import process_material_sheet
from labor import process_labor_sheet
from equipment import process_equipment_sheet
from config import config

wb = Workbook('./files/test.xlsx')

material = process_material_sheet(wb.worksheets['material'])
labor = process_labor_sheet(wb.worksheets['labor'])
equipment = process_equipment_sheet(wb.worksheets['equipment'])
print(labor)
print(equipment)
