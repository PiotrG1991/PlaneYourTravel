from django.contrib.auth.models import User
from django.db import models

class Accommodation(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)


class Transport(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    transport_cost = models.DecimalField(max_digits=10, decimal_places=2)


class Activity(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class TuristsPlaces(models.Model):
    description = models.TextField(null=True)


class Destination(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, null=True)
    accommodation= models.ForeignKey(Accommodation, on_delete=models.CASCADE, null=True)
    turists_places = models.ForeignKey(TuristsPlaces, on_delete=models.CASCADE, null=True)
    activity = models.ManyToManyField(Activity, null=True)


class Travel(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    participants = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=False)
