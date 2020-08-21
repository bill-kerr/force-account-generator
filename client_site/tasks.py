from celery import shared_task
from celery_progress.backend import ProgressRecorder
from pdf_generator import generate_pdf
from excel_importer import Importer


@shared_task(bind=True)
def generate_force_account(self, input_file, output_file_path):
    data = Importer(input_file).data
    generate_pdf(data, '../pdf_config.json', output_file_path)
    return 'Done'
