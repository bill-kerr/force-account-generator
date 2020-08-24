import os
from django.db import models


class UploadedFile(models.Model):
    docfile = models.FileField(upload_to='uploads')

    def __str__(self):
        return self.docfile.name

    @property
    def file_path(self):
        return os.path.realpath(self.docfile.name)
