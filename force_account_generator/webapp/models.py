import os
from django.db import models
from django.dispatch import receiver


class UploadedFile(models.Model):
    docfile = models.FileField(upload_to='uploads')

    def __str__(self):
        return self.docfile.name

    @property
    def file_path(self):
        return os.path.realpath(self.docfile.name)


@receiver(models.signals.post_delete, sender=UploadedFile)
def auto_delete_file(sender, instance, **kwargs):
    if instance.file_path:
        if os.path.isfile(instance.file_path):
            os.remove(instance.file_path)
