import json


def load_json_data(file_path):
    if not file_path.endswith('.json'):
        raise TypeError('Invalid JSON file.')
    try:
        with open(file_path) as f:
            data = json.load(f)
        return data
    except (FileNotFoundError, PermissionError):
        print('File does not exist or it is opened by another process.')
