"""
Program that creates a PDF force account package from JSON data.
JSON input data must be in the same format as input.example.json.
"""
import argparse
from pdf_config import PdfFieldConfig
from input_data import InputData
from material import MaterialCollection


def populate_work_schedule(work_schedule, units, resource_type):
    for unit_id, unit in units.items():
        for day in unit['daily_hours']:
            work_day = work_schedule.add_day(day['date'])
            if resource_type == "labor":
                work_day.add_labor(unit_id, unit, day.get('st'), day.get('ot'))
            elif resource_type == "equipment":
                work_day.add_equipment(
                    unit_id, unit, day.get('op'), day.get('sb'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'source', help='The path to the source JSON file (must end with .json)')
    parser.add_argument(
        'dest', help='The path to the destination PDF file (must end with .pdf)')
    args = parser.parse_args()

    if not args.source.endswith('.json') or not args.dest.endswith('.pdf'):
        raise parser.error(
            'Incorrect file extension (source=*.json dest=*.pdf)')

    pdf_config = PdfFieldConfig('./pdf_config.json')
    input_data = InputData(args.source)
    material_collection = MaterialCollection(pdf_config, input_data)

    # with open(args.source) as f:
    #     data = json.load(f)

    # material = create_dict(data['material']['data'])
    # labor = create_dict(data['labor']['data'])
    # equipment = create_dict(data['equipment']['data'])
    # rentals = create_dict(data['rentals']['data'])
    # services = create_dict(data['services']['data'])
    # stock_consumables = create_dict(data['stock_consumables']['data'])
    # purchased_consumables = create_dict(data['purchased_consumables']['data'])

    # ws = WorkSchedule()
    # populate_work_schedule(ws, labor, "labor")
    # populate_work_schedule(ws, equipment, "equipment")

    # pdf_config = PdfConfig()
    # pages = []

    # for work_day in ws.get_days().values():
    #     labor_hours, equip_hours = work_day.paginate(7, 4)
    #     for paginated_labor, paginated_equipment in zip(labor_hours, equip_hours):
    #         template = "./files/" + pdf_config.daily_config.template
    #         page = DailyPage(template, paginated_labor, paginated_equipment)
    #         pages.append(page)

    # make_pdf(pages, args.dest)
