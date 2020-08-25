import json
import os
import uuid


def load_json_data(json_file):
    try:
        data = json.load(json_file)
        return data
    except (FileNotFoundError, PermissionError):
        print('File does not exist or it is opened by another process.')


def gen_pdf_filename():
    return os.path.join(os.getcwd(), 'generated', f'{uuid.uuid4()}.pdf')
