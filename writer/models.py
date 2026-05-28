from django.db import models
from models.base import BaseDatabaseModel

class Writer(BaseDatabaseModel):
    writer = models.CharField(max_length=256)
    slug = models.SlugField(unique=True,blank=True)
    image = models.ImageField(upload_to='writer/')
    description = models.TextField()

    def __str__(self):
        return self.writer

