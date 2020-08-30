from django.core.files.base import ContentFile
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from pdf_generator import generate_pdf
from excel_importer import Importer
from .util import gen_filename
from .models import UploadedFile, ForceAccountPackage


@shared_task(bind=True)
def generate_force_account(self, file_object_id, daily_sheets=False):
    uploaded_file = UploadedFile.objects.get(id=file_object_id)
    callback = make_callback(ProgressRecorder(self))
    data = Importer(uploaded_file.docfile, callback=callback).data
    file_result = generate_pdf(data, daily_sheets=daily_sheets, callback=callback)
    package = ForceAccountPackage(task_id=self.request.id)
    package.docfile.save(gen_filename('pdf'), ContentFile(file_result.getvalue()))


def make_callback(progress_recorder):
    def progress_callback(status):
        stage = status.get('stage') or 0
        progress = (stage - 1) * 100 if stage != 0 else 0
        progress_recorder.set_progress(progress, 100, description=status)
    return progress_callback
