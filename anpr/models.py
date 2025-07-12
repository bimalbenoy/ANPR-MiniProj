from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class Residents(models.Model):
    CATEGORY_CHOICES = [
        ('Resident', 'Resident'),
        ('Visitor', 'Visitor'),
        ('Criminal', 'Criminal'),
    ]

    owner_name = models.CharField(max_length=100, default='Unknown')
    vehicle_number = models.CharField(max_length=100, unique=True)
    resident_address = models.TextField(default="Not Provided")
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Resident')
    registered_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.vehicle_number} - {self.owner_name}"

class Logbook(models.Model):
    CATEGORY_CHOICES = [
        ('Resident', 'Resident'),
        ('Visitor', 'Visitor'),
        ('Criminal', 'Criminal'),
    ]

    owner_name = models.CharField(max_length=100, default='Unknown')
    vehicle_number = models.CharField(max_length=100)
    resident_address = models.TextField(default="Not Provided")
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Resident')
    registered_date = models.DateField(auto_now_add=True)
    registered_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle_number} ({self.registered_date} {self.registered_time})"
