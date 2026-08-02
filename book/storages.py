from storages.backends.s3boto3 import S3Boto3Storage

class PublicMediaStorage(S3Boto3Storage):
    location = 'media/public'
    file_overwrite = False
    default_acl = None  # ACL istifadə etmirik, AWS Block Public ACL ilə toqquşmur

class PrivateMediaStorage(S3Boto3Storage):
    location = 'media/private'
    file_overwrite = False
    custom_domain = False
    default_acl = None
    querystring_auth = True  # Müvəqqəti imzalanmış linklər yaradır