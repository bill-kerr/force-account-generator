import json
from time import sleep
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from pdf_generator import generate_pdf
from excel_importer import Importer
from .util import load_json_data


@shared_task(bind=True)
def generate_force_account(self, input_file, output_file_path, daily_sheets=False, save_json=True):
    data = load_data(input_file, save_json)
    cb = make_callback(ProgressRecorder(self))
    generate_pdf(data, output_file_path, daily_sheets=daily_sheets, callback=cb)
    return 'Done'


def load_data(input_file, save_json):
    if input_file.endswith('.xlsx'):
        return Importer(input_file, save_json=save_json).data
    elif input_file.endswith('.json'):
        return load_json_data(input_file)

    raise TypeError('An invalid filetype was supplied.')


def make_callback(progress_recorder):
    def progress_callback(status):
        progress = status['progress'] * 100
        progress_recorder.set_progress(progress, 100, description=status)
    return progress_callback
