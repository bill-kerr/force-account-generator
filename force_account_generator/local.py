import sys
import random
import string
import os
from force_account_generator.excel_importer import Importer
from force_account_generator.pdf_generator import generate_pdf


def make_filename(file_path: str):
    base = os.path.basename(file_path)
    letters = string.ascii_lowercase
    random_str = ''.join(random.choice(letters) for _ in range(10))
    return os.path.splitext(base)[0].join(random_str + '.pdf')


if __name__ == 'main':
    if len(sys.argv) != 1:
        print('This program requires exactly one argument: The excel file name.')
    filename_arg = sys.argv[0]
    data = Importer(filename_arg).data
    file_result = generate_pdf(data, True)
    filename = make_filename(filename_arg)
    with open(filename, 'wb') as f:
        f.write(file_result.read())
