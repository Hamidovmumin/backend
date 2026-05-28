from django.db import models
from models.base import BaseDatabaseModel

class Tag(BaseDatabaseModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name