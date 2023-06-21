from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
from django.db.models import CharField


class Reservation(models.Model):
    user = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    reservation_date = models.DateTimeField()
    table_count = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1),MaxValueValidator(6)])
