"""
Program that extracts data from Excel to a JSON file for force account generation.
JSON data will be created in the same format as output.example.json.
"""
import json
import argparse
from workbook import Workbook


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='The path to the source Excel file (must end with .xlsx)')
    parser.add_argument('dest', help='The path to the destination JSON file (must end with .json)')
    args = parser.parse_args()

    if not args.source.endswith('.xlsx') or not args.dest.endswith('.json'):
        raise parser.error('Incorrect file extension (source=*.xlsx dest=*.json)')

    wb = Workbook(args.source)
    data = wb.process_workbook()

    with open(args.dest, 'w') as fp:
        json.dump(data, fp)
