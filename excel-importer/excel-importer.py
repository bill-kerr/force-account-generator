import sys
import json
from workbook import Workbook


if __name__ == '__main__':
    usage_message = 'Usage: excel-importer.py <./source.xlsx> [./result.json]'

    if len(sys.argv) < 2:
        raise Exception(usage_message)
    source = sys.argv[1]
    dest = ''./result.json'

    if len(sys.argv) > 2:
        dest = sys.argv[2]

    if not dest.endswith('.json'):
        raise Exception(usage_message)

    wb = Workbook(source)
    data = wb.process_workbook()

    with open(dest, 'w') as fp:
        json.dump(data, fp)
