import json
import os
import uuid
import boto3
from django.conf import settings


def load_json_data(json_file):
    try:
        data = json.load(json_file)
        return data
    except (FileNotFoundError, PermissionError):
        print('File does not exist or it is opened by another process.')


def gen_pdf_filename():
    return f'{uuid.uuid4().hex}.pdf'


def get_pdf_destination():
    if settings.USE_S3:
        def write_to_s3(file_result):
            s3 = boto3.resource('s3')
            obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, gen_pdf_filename())
            obj.put(Body=file_result)
        return write_to_s3
    else:
        return os.path.join(os.getcwd(), 'generated', gen_pdf_filename())
