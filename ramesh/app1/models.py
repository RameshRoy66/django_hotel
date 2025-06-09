from django.db import models
from django.utils import timezone


# Create your models here.

class Destinations(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='pics')
    description=models.TextField()
    price=models.IntegerField()
    days=models.IntegerField(null=True, blank=True)
    offer=models.BooleanField(default=False)


class Booking(models.Model):
    user_id = models.IntegerField()
    place = models.CharField(max_length=100)
    place_id = models.IntegerField()
    date = models.DateField()
    days = models.IntegerField()
    notes = models.TextField()
    # CORRECTED LINE
    created_date = models.DateTimeField(null=True, blank=True)
