from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION


class GeneratedStorage(S3Boto3Storage):
    location = settings.GENERATED_FILES_LOCATION


class UploadedStorage(S3Boto3Storage):
    location = settings.UPLOADED_FILES_LOCATION
