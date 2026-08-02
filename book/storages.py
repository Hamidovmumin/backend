from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    file_overwrite = False
    custom_domain = False