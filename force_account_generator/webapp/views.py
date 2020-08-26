from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .forms import UploadFileForm, GenerateForceAccountForm
from .tasks import generate_force_account
from .models import UploadedFile
from .util import gen_pdf_filename


def index(request):
    form = GenerateForceAccountForm()
    return render(request, 'webapp/index.html', {'form': form})


def process(request, task_id):
    return render(request, 'webapp/process.html', {'task_id': task_id})


def generate(request):
    if request.method == 'POST':
        form = GenerateForceAccountForm(request.POST, request.FILES)
        if form.is_valid():
            docfile = UploadedFile(docfile=request.FILES['docfile'])
            docfile.save()
            daily_sheets = form.cleaned_data['daily_sheets']
            dest_path = gen_pdf_filename()
            result = generate_force_account.delay(docfile.file_path, docfile.id, dest_path, daily_sheets=daily_sheets)
            return JsonResponse({'task_id': result.task_id})
    response = JsonResponse({'error': 'Bad request'})
    response.status_code = 400
    return response
