from django.contrib.gis.db import models

# Create your models here.


# Owner model
class Owner(models.Model):
    name = models.CharField(max_length=255)
    national_code = models.BigIntegerField(unique=True)
    age = models.PositiveIntegerField()
    total_toll_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

# Car model
class Car(models.Model):
    CAR_TYPES = (
        ('small', 'Small'),
        ('big', 'Big'),
    )
    owner = models.ForeignKey(Owner, related_name='cars', on_delete=models.CASCADE)
    car_type = models.CharField(max_length=10, choices=CAR_TYPES)
    color = models.CharField(max_length=50)
    length = models.FloatField()
    load_volume = models.FloatField(null=True, blank=True)  # فقط برای خودروهای سنگین

    def __str__(self):
        return f"{self.car_type} - {self.color}"

# Road model
class Road(models.Model):
    name = models.CharField(max_length=255)
    width = models.FloatField()
    geom = models.MultiLineStringField()

    def __str__(self):
        return self.name

# TollStation model
class TollStation(models.Model):
    name = models.CharField(max_length=255)
    toll_per_cross = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.PointField()

    def __str__(self):
        return self.name

# CarMovement model
class CarMovement(models.Model):
    car = models.ForeignKey(Car, related_name='movements', on_delete=models.CASCADE)
    location = models.PointField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.car} at {self.date}"