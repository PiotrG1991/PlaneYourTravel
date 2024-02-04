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


class TuristsPlaces(models.Model):
    description = models.BigAutoField


class Destination(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    accommodation= models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    turists_places = models.ForeignKey(TuristsPlaces, on_delete=models.CASCADE)
    activity = models.ManyToManyField(Activity)


class Travel(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    participants = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
