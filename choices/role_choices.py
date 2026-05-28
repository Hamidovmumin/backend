from django.db import models

class Role(models.TextChoices):
    author = 'Author',
    editor= 'Editor',
    translator = 'Translator'