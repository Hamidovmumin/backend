from django.db import models

class Currency(models.TextChoices):
    AZN = 'AZN', 'Azerbaijan Manat'
    USD = 'USD', 'US Dollar'
    EUR = 'EUR', 'Euro'