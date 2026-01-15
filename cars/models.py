from django.db import models
from django.contrib.auth.models import User


class Vehicle(models.Model):
    TYPE = [('car', 'Car'), ('bike', 'Bike')]
    CONDITION = [('new', 'New'), ('old', 'Old')]
    FUEL = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]
    TRANSMISSION = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]

    # Basic
    brand = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='vehicles/')
    vehicle_type = models.CharField(max_length=10, choices=TYPE)
    condition = models.CharField(max_length=10, choices=CONDITION)

    # Fuel & Performance
    fuel_type = models.CharField(max_length=10, choices=FUEL)
    mileage = models.FloatField(help_text="km/l or km/charge")
    transmission = models.CharField(max_length=10, choices=TRANSMISSION)

    # Engine / Battery
    engine_cc = models.IntegerField(null=True, blank=True)
    battery_capacity = models.FloatField(null=True, blank=True, help_text="kWh")
    power = models.IntegerField(null=True, blank=True, help_text="bhp")

    # Old vehicle details
    year = models.IntegerField(null=True, blank=True)
    km_driven = models.IntegerField(null=True, blank=True)
    ownership = models.CharField(max_length=50, null=True, blank=True)
    insurance_valid = models.BooleanField(default=False)

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
