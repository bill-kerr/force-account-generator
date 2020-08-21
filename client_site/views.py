from django.shortcuts import render
from openpyxl import load_workbook
from .forms import UploadFileForm
from .tasks import generate_force_account

# Create your views here.


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid form')
            print(request.FILES['docfile'])
            generate_force_account.delay(request.FILES['docfile'], './output.pdf')
    else:
        form = UploadFileForm()

    return render(request, 'client_site/index.html', {'form': form})
