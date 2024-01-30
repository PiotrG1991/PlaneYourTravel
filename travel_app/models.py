from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Travel(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    participants = models.CharField(max_length=255)

class Destination(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE)

class Cost(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    destination = models.ManyToManyField(Destination)

class Vehicle(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

class Accomodation(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

class Activity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    destination = models.ForeignKey(Travel, on_delete=models.CASCADE)

