"""
Program that creates a PDF force account package from JSON data.
JSON input data must be in the same format as input.example.json.
"""
import argparse
import json
from util import create_dict
from work_schedule import WorkSchedule


def populate_work_schedule(work_schedule, units, is_labor=True):
    for unit_id, unit in units.items():
        for day in unit['daily_hours']:
            work_day = work_schedule.add_day(day['date'])
            if is_labor:
                work_day.add_labor(unit_id, day.get('st'), day.get('ot'))
            else:
                work_day.add_equipment(unit_id, day.get('op'), day.get('sb'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='The path to the source JSON file (must end with .json)')
    parser.add_argument('dest', help='The path to the destination PDF file (must end with .pdf)')
    args = parser.parse_args()

    if not args.source.endswith('.json') or not args.dest.endswith('.pdf'):
        raise parser.error('Incorrect file extension (source=*.json dest=*.pdf)')

    with open(args.source) as f:
        data = json.load(f)

    material = create_dict(data['material']['data'])
    labor = create_dict(data['labor']['data'])
    equipment = create_dict(data['equipment']['data'])
    rentals = create_dict(data['rentals']['data'])
    services = create_dict(data['services']['data'])
    stock_consumables = create_dict(data['stock_consumables']['data'])
    purchased_consumables = create_dict(data['purchased_consumables']['data'])

    ws = WorkSchedule()
    populate_work_schedule(ws, labor)
    populate_work_schedule(ws, equipment, is_labor=False)

    for day in ws.get_days().values():
        labor_hours, equip_hours = day.paginate(7, 4)
        print(len(labor_hours), len(equip_hours))
