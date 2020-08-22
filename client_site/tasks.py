import json
from time import sleep
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from pdf_generator import generate_pdf
from excel_importer import Importer


@shared_task(bind=True)
def generate_force_account(self, input_file, output_file_path):
    # data = Importer(input_file).data
    data = load_test_data()
    cb = make_callback(ProgressRecorder(self))
    generate_pdf(data, 'pdf_config.json', output_file_path, daily_sheets=True, callback=cb)
    return 'Done'


def load_test_data():
    with open('E:\\dev\\force-account-generator\\pdf_generator\\files\\output20200819.json') as f:
        data = json.load(f)
    return data


def make_callback(progress_recorder):
    def progress_callback(status):
        progress = status['progress'] * 100
        progress_recorder.set_progress(progress, 100, description=status)
    return progress_callback
