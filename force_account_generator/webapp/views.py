import os
import json
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from .tasks import generate_force_account


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_path = os.path.join(os.getcwd(), 'files', 'output20200819.json')
            result = generate_force_account.delay(file_path, './files/output.pdf')
            return render(request, 'webapp/index.html', {'task_id': result.task_id})
    else:
        form = UploadFileForm()

    return render(request, 'webapp/index.html', {'form': form})
