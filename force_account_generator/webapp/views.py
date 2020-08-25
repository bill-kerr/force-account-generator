from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .forms import UploadFileForm, GenerateForceAccountForm
from .tasks import generate_force_account
from .models import UploadedFile
from .util import gen_pdf_filename


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            daily_sheets = form.cleaned_data['daily_sheets']
            docfile = UploadedFile(docfile=request.FILES['docfile'])
            docfile.save()
            dest_path = gen_pdf_filename()
            result = generate_force_account.delay(docfile.file_path, docfile.id, dest_path, daily_sheets=daily_sheets)
            form = UploadFileForm()
            return HttpResponseRedirect(f'/process/{result.task_id}')
    else:
        form = UploadFileForm()

    return render(request, 'webapp/index.html', {'form': form})


def process(request, task_id):
    return render(request, 'webapp/process.html', {'task_id': task_id})


def generate(request):
    if request.method == 'POST':
        form = GenerateForceAccountForm(request.POST)
        if form.is_valid():
            file_id = form.cleaned_data['file_id']
            docfile = UploadedFile.objects.get(pk=file_id)
            daily_sheets = form.cleaned_data['daily_sheets']
            dest_path = gen_pdf_filename()
            result = generate_force_account.delay(docfile.file_path, docfile.id, dest_path, daily_sheets=daily_sheets)
            return JsonResponse({'task_id': result.task_id})


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            docfile = UploadedFile(docfile=request.FILES['docfile'])
            docfile.save()
            return JsonResponse({'file_id': docfile.id})
    return HttpResponseRedirect('/')
