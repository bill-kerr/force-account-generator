import sys
import json
from workbook import Workbook
from materials import process_material_sheet
from labor import process_labor_sheet
from equipment import process_equipment_sheet
from rentals import process_rental_sheet
from services import process_service_sheet
from purchased_consumables import process_purchased_consumables_sheet
from stock_consumables import process_stock_consumables_sheet
from config import Config


def process_sheet(file_path):
    wb = Workbook(file_path)

    data = {}
    data.update(get_defined_cell_data(wb))

    data['material'] = process_material_sheet(wb.worksheets['material'])
    data['labor'] = process_labor_sheet(wb.worksheets['labor'])
    data['equipment'] = process_equipment_sheet(wb.worksheets['equipment'])
    data['rentals'] = process_rental_sheet(wb.worksheets['rentals_and_service_by_others'])
    data['services'] = process_service_sheet(wb.worksheets['rentals_and_service_by_others'])
    data['purchased_consumables'] = process_purchased_consumables_sheet(wb.worksheets['consumables'])
    data['stock_consumables'] = process_stock_consumables_sheet(wb.worksheets['consumables'])

    return json.dumps(data)


def get_defined_cell_data(workbook):
    print(workbook.defined_cells)
    data = {}
    data['county'] = workbook.defined_cells['summary'][Config.defined_cells['county']]
    data['state_route'] = workbook.defined_cells['summary'][Config.defined_cells['state_route']]
    data['section'] = workbook.defined_cells['summary'][Config.defined_cells['section']]
    data['work_order_number'] = workbook.defined_cells['summary'][Config.defined_cells['work_order_number']]
    data['contract'] = workbook.defined_cells['summary'][Config.defined_cells['contract']]
    data['item_number'] = workbook.defined_cells['summary'][Config.defined_cells['item_number']]
    data['prime_contractor'] = workbook.defined_cells['summary'][Config.defined_cells['prime_contractor']]
    data['statement_of_cost'] = workbook.defined_cells['summary'][Config.defined_cells['statement_of_cost']]
    return data


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('A file path must be entered as a command line argument.')
    file_path = sys.argv[1]
    process_sheet(file_path)
