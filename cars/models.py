from django.db import models
from django.contrib.auth.models import User

class Vehicle(models.Model):
    TYPE = [('car','Car'), ('bike','Bike')]
    CONDITION = [('new','New'), ('old','Old')]

    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='vehicles/')
    vehicle_type = models.CharField(choices=TYPE, max_length=10)
    condition = models.CharField(choices=CONDITION, max_length=10)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class SellExchange(models.Model):
    TYPE = [('car','Car'), ('bike','Bike')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_type = models.CharField(choices=TYPE, max_length=10)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.IntegerField()
    exchange = models.BooleanField(default=False)


class LoanRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    amount = models.IntegerField()
    tenure = models.IntegerField()
    contact = models.CharField(max_length=15)

