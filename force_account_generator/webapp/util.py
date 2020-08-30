import json
import uuid


def load_json_data(json_file):
    try:
        data = json.load(json_file)
        return data
    except (FileNotFoundError, PermissionError):
        print('File does not exist or it is opened by another process.')


def gen_filename(extension, prefix=''):
    return f'{prefix}{uuid.uuid4().hex}.{extension}'
