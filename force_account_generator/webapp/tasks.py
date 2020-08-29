import uuid
from django.core.files.base import ContentFile
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from pdf_generator import generate_pdf
from excel_importer import Importer
from .util import load_json_data
from .models import UploadedFile, ForceAccountPackage


@shared_task(bind=True)
def generate_force_account(self, input_file_path, file_object_id, daily_sheets=False):
    callback = make_callback(ProgressRecorder(self))
    data = load_data(input_file_path, callback=callback)
    file_result = generate_pdf(data, daily_sheets=daily_sheets, callback=callback)
    package = ForceAccountPackage(task_id=self.request.id)
    package.docfile.save(gen_filename('pdf'), ContentFile(file_result.getvalue()))
    UploadedFile.objects.get(id=file_object_id).delete()


def load_data(file_path, callback=None):
    if file_path.endswith('.xlsx'):
        return Importer(file_path, callback=callback).data

    if file_path.endswith('.json'):
        return load_json_data(file_path)

    raise TypeError('An invalid filetype was supplied.')


def make_callback(progress_recorder):
    def progress_callback(status):
        stage = status.get('stage') or 0
        progress = (stage - 1) * 100 if stage != 0 else 0
        progress_recorder.set_progress(progress, 100, description=status)
    return progress_callback


def gen_filename(extension, prefix=''):
    return f'{prefix}{uuid.uuid4().hex}.{extension}'
