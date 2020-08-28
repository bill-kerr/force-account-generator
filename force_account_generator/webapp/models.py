import os
from django.db import models
from django.dispatch import receiver
from django.conf import settings


class UploadedFile(models.Model):
    docfile = models.FileField(upload_to='uploads')

    def __str__(self):
        return self.docfile.name


class ForceAccountPackage(models.Model):
    docfile = models.FileField()
    task_id = models.UUIDField(blank=False)

    def __str__(self):
        return self.docfile.name


@receiver(models.signals.post_delete, sender=UploadedFile)
def auto_delete_file(sender, instance, **kwargs):
    if instance.file_path:
        if os.path.isfile(instance.file_path):
            os.remove(instance.file_path)
