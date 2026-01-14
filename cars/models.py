from django.db import models
from django.contrib.auth.models import User

class Vehicle(models.Model):
    TYPE = [('car', 'Car'), ('bike', 'Bike')]
    CONDITION = [('new', 'New'), ('old', 'Old')]

    brand = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='vehicles/')
    vehicle_type = models.CharField(max_length=10, choices=TYPE)
    condition = models.CharField(max_length=10, choices=CONDITION)

    def __str__(self):
        return f"{self.brand} {self.name}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class SellExchange(models.Model):
    TYPE = [('car', 'Car'), ('bike', 'Bike')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=10, choices=TYPE)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    description = models.TextField()
    price = models.IntegerField()
    exchange = models.BooleanField(default=False)


class LoanRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    amount = models.IntegerField()
    tenure = models.IntegerField()
    contact = models.CharField(max_length=15)
