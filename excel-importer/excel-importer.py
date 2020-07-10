from workbook import Workbook
from materials import process_material_sheet
from labor import process_labor_sheet
from equipment import process_equipment_sheet
from rentals import process_rental_sheet
from services import process_service_sheet
from config import config

wb = Workbook('./files/test.xlsx')

material = process_material_sheet(wb.worksheets['material'])
labor = process_labor_sheet(wb.worksheets['labor'])
equipment = process_equipment_sheet(wb.worksheets['equipment'])
rentals = process_rental_sheet(wb.worksheets['rentals_and_service_by_others'])
services = process_service_sheet(wb.worksheets['rentals_and_service_by_others'])
