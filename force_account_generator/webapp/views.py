import os
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import GenerateForceAccountForm
from .tasks import generate_force_account
from .models import UploadedFile, ForceAccountPackage


def index(request):
    form = GenerateForceAccountForm()
    return render(request, 'webapp/index.html', {'form': form})


def generate(request):
    if request.method == 'POST':
        form = GenerateForceAccountForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = UploadedFile()
            uploaded_file.docfile.save(request.FILES['docfile'].name, request.FILES['docfile'])
            daily_sheets = form.cleaned_data['daily_sheets']
            result = generate_force_account.delay(uploaded_file.id, daily_sheets=daily_sheets)
            return JsonResponse({'task_id': result.task_id})
    response = JsonResponse({'error': 'Bad request'})
    response.status_code = 400
    return response


def packages(request, task_id):
    package = get_object_or_404(ForceAccountPackage, task_id=task_id)
    response = HttpResponse(package.docfile, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={package.docfile}'
    return response


def about(request):
    return render(request, 'webapp/about.html')


def demo(request):
    file_id = os.environ.get('DEMO_FILE_ID')
    print(file_id)
    result = generate_force_account.delay(file_id)
    return JsonResponse({'task_id': result.task_id})
