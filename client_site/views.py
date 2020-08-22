from django.shortcuts import render
from django.http import HttpResponseRedirect
from openpyxl import load_workbook
from .forms import UploadFileForm
from .tasks import generate_force_account
from client.celery import debug_task

# Create your views here.


def index(request):
    if request.method == 'POST':
        print(request.method)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            result = generate_force_account.delay('input file path', './files/output.pdf')
    else:
        form = UploadFileForm()

    return render(request, 'client_site/index.html', {'form': form, 'task_id': result.task_id})
