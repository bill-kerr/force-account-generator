import os
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import UploadFileForm, GenerateForceAccountForm
from .tasks import generate_force_account
from .models import UploadedFile, ForceAccountPackage
from .util import gen_pdf_filename


def index(request):
    form = GenerateForceAccountForm()
    return render(request, 'webapp/index.html', {'form': form})


def generate(request):
    if request.method == 'POST':
        form = GenerateForceAccountForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = UploadedFile(docfile=request.FILES['docfile'])
            uploaded_file.save()
            docfile = uploaded_file.docfile
            daily_sheets = form.cleaned_data['daily_sheets']
            dest_path = gen_pdf_filename()
            result = generate_force_account.delay(docfile.path, uploaded_file.id, dest_path, daily_sheets=daily_sheets)
            return JsonResponse({'task_id': result.task_id})
    response = JsonResponse({'error': 'Bad request'})
    response.status_code = 400
    return response


def packages(request, task_id):
    package = get_object_or_404(ForceAccountPackage, task_id=task_id)
    filename = os.path.basename(package.docfile.name)
    response = HttpResponse(package.docfile, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


def about(request):
    return render(request, 'webapp/about.html')
