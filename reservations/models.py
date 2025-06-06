from django.db import models
from datetime import date
from django.core.exceptions import ValidationError

# Create your models here.
def validate_dates(value):
    if value <= date.today():
        raise ValidationError("Date must be greater than current date.")

class Reservation(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date = models.DateField(validators=[validate_dates])
    party_size = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True)
    notes = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"