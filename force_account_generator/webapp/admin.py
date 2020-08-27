from django.contrib import admin
from .models import UploadedFile, ForceAccountPackage

# Register your models here.
admin.site.register(UploadedFile)
admin.site.register(ForceAccountPackage)
