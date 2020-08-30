import os
from django.db import models
from django.dispatch import receiver
from custom_storages import GeneratedStorage, UploadedStorage


class UploadedFile(models.Model):
    docfile = models.FileField(storage=UploadedStorage())

    def __str__(self):
        return self.docfile.name

    @property
    def file_path(self):
        return os.path.realpath(self.docfile.name)


class ForceAccountPackage(models.Model):
    docfile = models.FileField(storage=GeneratedStorage())
    task_id = models.UUIDField(blank=False)

    def __str__(self):
        return f'{self.id} ({self.task_id})'


@receiver(models.signals.post_delete, sender=UploadedFile)
def auto_delete_file(sender, instance, **kwargs):
    if instance.docfile:
        if os.path.isfile(instance.file_path):
            os.remove(instance.file_path)
