import os
from django.db import models
from django.dispatch import receiver
from custom_storages import GeneratedStorage, UploadedStorage


class UploadedFile(models.Model):
    docfile = models.FileField(storage=UploadedStorage())
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} ({self.docfile.name})'


class ForceAccountPackage(models.Model):
    docfile = models.FileField(storage=GeneratedStorage())
    task_id = models.UUIDField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} ({self.task_id})'


@receiver(models.signals.post_delete, sender=UploadedFile)
def auto_delete_file(sender, instance, **kwargs):
    if instance.docfile:
        if os.path.isfile(instance.path):
            os.remove(instance.path)
