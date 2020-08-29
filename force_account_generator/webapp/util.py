import json


def load_json_data(json_file):
    try:
        data = json.load(json_file)
        return data
    except (FileNotFoundError, PermissionError):
        print('File does not exist or it is opened by another process.')
