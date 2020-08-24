import os
import uuid
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .tasks import generate_force_account
from .models import UploadedFile


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            docfile = UploadedFile(docfile=request.FILES['docfile'])
            docfile.save()
            dest_path = os.path.join(os.getcwd(), 'generated', f'{uuid.uuid4()}.pdf')
            result = generate_force_account.delay(docfile.file_path, docfile.id, dest_path)
            return HttpResponseRedirect(f'/process/{result.task_id}')
    else:
        form = UploadFileForm()

    return render(request, 'webapp/index.html', {'form': form})


def process(request, task_id):
    return render(request, 'webapp/process.html', {'task_id': task_id})
